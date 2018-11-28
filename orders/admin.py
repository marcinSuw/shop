from django.contrib import admin

from orders.models import Cart, Order, OrderItem


class CartAdmin(admin.ModelAdmin):
    pass


class OrderItemAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
