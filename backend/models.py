from django.db import models
from django.utils.text import slugify
import re
from django.core.validators import RegexValidator

COLOR_VALIDATOR = RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'only valid hex color code is accepted')

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='uploads/categories/')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


# This is for example mc, vim number fields of the product
class LetteringItemCategory(models.Model):
    title = models.CharField(max_length=256)
    price = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = 'lettering item categories'

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    base_price = models.FloatField(default=0.0)
    # -1 means any possitive amount
    max_amount_of_lettering_items = models.FloatField(default=-1)
    image = models.ImageField(upload_to='uploads/products/')
    only_on_default_color = models.BooleanField(default=True)

    def __str__(self):
        return self.title + " - " + self.category.title


class ProductColor(models.Model):
    color_in_hex = models.CharField(max_length=256, validators=[COLOR_VALIDATOR], default='#000000')
    color_nickname = models.CharField(max_length=256,default='add nickname')

    def __str__(self):
        return self.color_nickname


class ProductVariation(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True)

    def get_all_lettering_items(self):
        return self.letteringitemvariation__set.objects.all()

    def get_total_price(self):
        items = self.get_all_lettering_items()
        price = self.product__base_price()
        for item in items:
            price += item.lettering_item_category.price
        return price

    def __str__(self):
        return self.product.title + str(self.id)

class LetteringItemVariation(models.Model):
    lettering_item_category = models.ForeignKey(LetteringItemCategory, on_delete=models.CASCADE)
    lettering = models.CharField(max_length=256)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)

    def __str__(self):
        return self.lettering_item_category.title + " - " + self.lettering



class Payment(models.Model):
    user_email = models.CharField(max_length=256)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_email + " - " + self.timestamp



class Order(models.Model):
    ordered_date = models.DateField(auto_now_add=True)
    user_email = models.CharField(max_length=256)
    user_first_name = models.CharField(max_length=256)
    user_last_name = models.CharField(max_length=256)
    # send_email_proof = models.BooleanField(default=False)
    address1 = models.CharField(max_length=1024, default='Address line 1')
    address2 = models.CharField(max_length=1024, blank=True, null=True, default='Address line 2')
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user_email + '-' + str(self.ordered_date)

    def get_total_price(self):
        return self.product.get_total_price()



# class ProductType(models.Model):
#     name_of_type_of_product = models.CharField(max_length=256, default='Truck Logo', unique=True)
#     single_image = models.ImageField(upload_to='uploads/products_types/')
#     base_price = models.FloatField(default=0.0)
#
#     is_company_name_enable = models.BooleanField(default=False)
#     company_name_price = models.FloatField(default=0.0)
#
#     is_dot_number_enable = models.BooleanField(default=False)
#     dot_number_price = models.FloatField(default=0.0)
#
#     is_mc_number_enable = models.BooleanField(default=False)
#     mc_number_price = models.FloatField(default=0.0)
#
#     is_origin_enable = models.BooleanField(default=False)
#     origin_price = models.FloatField(default=0.0)
#
#     is_vim_number_enable = models.BooleanField(default=False)
#     vim_number_price = models.FloatField(default=0.0)
#
#     is_truck_number_enable = models.BooleanField(default=False)
#     truck_number_price = models.FloatField(default=0.0)
#
#     is_color_enable = models.BooleanField(default=False)
#     color_price = models.FloatField(default=0.0)
#
#
#     # def save(self, *args, **kwargs):
#     #     if not self.id:
#     #         self.slug = slugify(str(self.type_of_product + self.id))
#     #     super(Product,self).save(*args, **kwargs)
#
#     def __str__(self):
#         return self.name_of_type_of_product

# class Product(models.Model):
#     type_of_product = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
#     single_image = models.ImageField(upload_to='uploads/products/single_images')
#     order_image = models.ImageField(upload_to='uploads/products/order_images')
#     is_single_image_for_show = models.BooleanField(default=True)
#
#
#     # def save(self, *args, **kwargs):
#     #     if not self.id:
#     #         self.slug = slugify(str(self.type_of_product + self.id))
#     #     super(Product,self).save(*args, **kwargs)
#
#     def __str__(self):
#         return self.type_of_product.name_of_type_of_product + ' ' + str(self.pk)






#  Skeleton of the complete order
# class Order(models.Model):
#     order_date_made = models.DateField(auto_now_add=True)
#     total_cost = models.FloatField(default=0.0)
#     user_email = models.CharField(max_length=256)
#     user_first_name = models.CharField(max_length=256)
#     user_last_name = models.CharField(max_length=256)
#     # slug = models.SlugField(blank=True)
#     send_email_proof = models.BooleanField(default=False)
#     # shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True)
#
#     address1 = models.CharField(max_length=1024, default='Address line 1')
#     address2 = models.CharField(max_length=1024, blank=True, null=True, default='Address line 2')
#     city = models.CharField(max_length=60, default="Miami")
#     state = models.CharField(max_length=30, default="Florida")
#     zipcode = models.CharField(max_length=5, default="33165")
#     country = models.CharField(max_length=50, default='USA')
#
#     order_is_complete = models.BooleanField(default=False)
#
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
#     product_type = models.CharField(blank=True,max_length=256)
#     product_color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True)
#     company_name = models.CharField(blank=True,max_length=256)
#     dot_number = models.CharField(blank=True,max_length=256)
#     mc_number = models.CharField(blank=True,max_length=256)
#     origin = models.CharField(blank=True,max_length=256)
#     vin_number = models.CharField(blank=True,max_length=256)
#     truck_number = models.CharField(blank=True,max_length=256)
#
#     comments = models.CharField(blank=True,max_length=256)
#
#     # def save(self, *args, **kwargs):
#     #     if not self.id:
#     #         slug_str = "%s %s" % (self.user_email, self.order_date_made)
#     #         unique_slugify(self, slug_str)
#     #     super(OrderItem, self).save(*args,**kwargs)
#
#     def __str__(self):
#         return self.user_email + '-' + str(self.order_date_made)
#
#









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
