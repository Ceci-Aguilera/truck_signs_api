from django.db import models

# Create your models here.

#Truck Item to sell
class TruckItem(models.Model):
    nickname = models.CharField(max_length=256)
    singleImage = models.ImageField(upload_to='uploads/trucks/singleImages')
    multiImage = models.ImageField(upload_to='uploads/trucks/multiImages')
    is_single_image_for_show = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname

#Other Products Item to sell
class OtherProduct(models.Model):
    nickname = models.CharField(max_length=256)
    singleImage = models.ImageField(upload_to='uploads/other_products/singleImages')
    multiImage = models.ImageField(upload_to='uploads/other_products/multiImages')
    is_single_image_for_show = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname
