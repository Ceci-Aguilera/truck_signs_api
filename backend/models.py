from django.db import models
from django.utils.text import slugify
import re

# Create your models here.

#Truck Item to sell
class TruckItem(models.Model):
    nickname = models.CharField(max_length=256, unique=True)
    singleImage = models.ImageField(upload_to='uploads/trucks/singleImages')
    multiImage = models.ImageField(upload_to='uploads/trucks/multiImages')
    is_single_image_for_show = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    price = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nickname)
        super(TruckItem,self).save(*args, **kwargs)

    def __str__(self):
        return self.nickname

#Other Products Item to sell
class OtherProduct(models.Model):
    nickname = models.CharField(max_length=256)
    singleImage = models.ImageField(upload_to='uploads/other_products/singleImages')
    multiImage = models.ImageField(upload_to='uploads/other_products/multiImages')
    is_single_image_for_show = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    price = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nickname)
        super(OtherProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.nickname

#Order any Item
class OrderItem(models.Model):
    order_date_made = models.DateField(auto_now_add=True)
    total_cost = models.FloatField(default=0.0)
    user = models.CharField(max_length=256)
    slug = models.SlugField(blank=True)
    send_email_proof = models.BooleanField(default=False)

    order_is_complete = models.BooleanField(default=False)

    has_truck_item = models.BooleanField(default=False)
    truck = models.ForeignKey(TruckItem, on_delete=models.SET_NULL, null=True)

    truck_color = models.CharField(blank=True,max_length=256)
    company_name = models.CharField(blank=True,max_length=256)
    dot_number = models.CharField(blank=True,max_length=256)
    mc_number = models.CharField(blank=True,max_length=256)
    origin = models.CharField(blank=True,max_length=256)
    vin_number = models.CharField(blank=True,max_length=256)

    has_truck_number = models.BooleanField(default=False)
    truck_number = models.CharField(blank=True,max_length=256)

    has_fire_Extinguisher = models.BooleanField(default=False)

    comments = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            slug_str = "%s %s" % (self.user, self.order_date_made)
            unique_slugify(self, slug_str)
        super(OrderItem, self).save(*args,**kwargs)

    def __str__(self):
        return self.user + '-' + str(self.order_date_made)


# UNIQUE SLUGIFY
def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
