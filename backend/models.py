from django.db import models
from django.utils.text import slugify
import re
from django.core.validators import RegexValidator

COLOR_VALIDATOR = RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'only valid hex color code is accepted')

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='uploads/categories/')
    base_price = models.FloatField(default=0.0)
    # -1 means any possitive amount
    max_amount_of_lettering_items = models.IntegerField(default=-1)

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
    image = models.ImageField(upload_to='uploads/products/')
    only_on_default_color = models.BooleanField(default=True)
    is_uploaded = models.BooleanField(default=False)

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
    amount = models.IntegerField(default=1)

    def get_all_lettering_items(self):
        return self.lettering_item_variation_set.all()

    def get_total_price(self):
        items = self.get_all_lettering_items()
        price = self.product.base_price
        for item in items:
            price += item.lettering_item_category.price
        price = price * self.amount
        return price

    def __str__(self):
        return self.product.title + " - " + str(self.id)

class LetteringItemVariation(models.Model):
    lettering_item_category = models.ForeignKey(LetteringItemCategory, on_delete=models.CASCADE)
    lettering = models.CharField(max_length=256)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE,related_name="lettering_item_variation_set")

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


class Comment(models.Model):
    user_email = models.CharField(max_length=256)
    image = models.ImageField(upload_to='uploads/comments/')
    text = models.TextField(blank=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.user_email
