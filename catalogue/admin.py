from django.contrib import admin
from .models import Item, Order, OrderItem, Address, Category


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    list_display = [
        'title',
        'price',
        'discount_price'
    ]


class OrderItemAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'item',
        'ordered',
        'quantity',
    ]


class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'ordered',
        'start_date',
        'ordered_date',
        'address'
    ]


class AddressAdmin(admin.ModelAdmin):
    
    list_display = [
        'street_address',
        'apartment_address',
        'country',
        'zip_code',
        'default',
        'use_default',
        'payment_option',
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]

admin.site.register(Item, ItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Category)
