from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from shopapp.models import Category, Product, Customer, Order, Profile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)

#mix profile info with user info
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
#extend user moodel
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]
#unregister
admin.site.unregister(User)

#then register
admin.site.register(User, UserAdmin)

