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
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    shipping_address = models.TextField(max_length=15000, null=True, blank=True)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=20)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {str(self.id)}'



#order items model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    price = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Order Item {str(self.id)}'
