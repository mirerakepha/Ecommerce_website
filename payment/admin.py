from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib import admin
from django.contrib.auth.models import User


#register the model on the admin section
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


#create an order item inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    readonly_fields = ["order_date"]
    extra = 0

    def order_date(self, obj):
        return obj.order.date_ordered   # pull from parent Order
    order_date.short_description = "Date Ordered"

    #extend the order item
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]

admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)