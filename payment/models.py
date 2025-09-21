from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from shopapp.models import Product

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_fullname = models.CharField(max_length=100, null=True, blank=True)
    shipping_email = models.EmailField(max_length=100, null=True, blank=True)
    shipping_street = models.CharField(max_length=100, null=True, blank=True)
    shipping_city = models.CharField(max_length=100, null=True, blank=True)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=100, null=True, blank=True)
    shipping_country = models.CharField(max_length=100, null=True, blank=True)
    shipping_phone = models.CharField(max_length=100, null=True, blank=True)


    #address ->dont pluralize it
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address {str(self.id)}'


#order model





#order items model
