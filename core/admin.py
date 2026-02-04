from django.contrib import admin
from django.utils.html import format_html

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


def update_order_status_shipped(modeladmin, request, queryset):
    queryset.update(status='shipped', being_delivered=True)


update_order_status_shipped.short_description = '将订单状态更新为已发货'


def update_order_status_delivering(modeladmin, request, queryset):
    queryset.update(status='delivering')


update_order_status_delivering.short_description = '将订单状态更新为配送中'


def update_order_status_completed(modeladmin, request, queryset):
    queryset.update(status='completed', received=True)


update_order_status_completed.short_description = '将订单状态更新为已完成'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'status',
                    'cancelled',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'status',
                   'cancelled',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted, update_order_status_shipped,
               update_order_status_delivering, update_order_status_completed]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'stock_threshold', 'stock_status_display']
    list_filter = ['category', 'label']
    search_fields = ['title', 'description']

    def stock_status_display(self, obj):
        if obj.stock <= 0:
            return format_html('<span style="color: red; font-weight: bold;">缺货</span>')
        elif obj.is_low_stock():
            return format_html('<span style="color: orange; font-weight: bold;">库存不足</span>')
        return format_html('<span style="color: green;">库存充足</span>')
    stock_status_display.short_description = '库存状态'


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
