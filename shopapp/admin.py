from django.contrib import admin

from shopapp.models import Category, Product, Customer, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
