from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s profile"



class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.name}"
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Product(models.Model):
         name = models.CharField(max_length=150)
         price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
         category = models.ForeignKey(Category, on_delete=models.CASCADE)
         description = models.TextField(max_length=250, default='', blank=True, null=True)
         image = models.ImageField(upload_to="products")
         def __str__(self):
            return f"{self.name}"


class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    password1 = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=150, default='', blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=150, default='', blank=True, null=True)
    email = models.EmailField(max_length=150, default='', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.customer.name}"
    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-date']
        permissions = (
            ('can_order', 'Can order'),
            ('can_cancel', 'Can cancel'),
            ('can_delete', 'Can delete'),
            ('can_purchase', 'Can purchase'),
            ('can_purchase_order', 'Can purchase order')
        )

