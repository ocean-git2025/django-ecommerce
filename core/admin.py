from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, ORDER_STATUS_CHOICES


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


def make_shipped(modeladmin, request, queryset):
    for order in queryset.filter(status='PENDING'):
        order.status = 'SHIPPED'
        order.being_delivered = True
        order.save()


make_shipped.short_description = '标记为已发货'


def make_delivering(modeladmin, request, queryset):
    for order in queryset.filter(status='SHIPPED'):
        order.status = 'DELIVERING'
        order.being_delivered = True
        order.save()


make_delivering.short_description = '标记为配送中'


def make_completed(modeladmin, request, queryset):
    for order in queryset.filter(status='DELIVERING'):
        order.status = 'COMPLETED'
        order.received = True
        order.save()


make_completed.short_description = '标记为已完成'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['ref_code',
                    'user',
                    'ordered',
                    'status',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon',
                    'ordered_date'
                    ]
    list_display_links = [
        'ref_code',
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'status',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted',
                   'ordered_date']
    list_editable = ['status']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted, make_shipped, make_delivering, make_completed]
    list_per_page = 20


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


class LowStockFilter(admin.SimpleListFilter):
    title = '库存状态'
    parameter_name = 'stock_status'

    def lookups(self, request, model_admin):
        return (
            ('low', '库存预警'),
            ('normal', '库存正常'),
            ('out', '缺货'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(stock__lte=models.F('stock_threshold'))
        elif self.value() == 'normal':
            return queryset.filter(stock__gt=models.F('stock_threshold'))
        elif self.value() == 'out':
            return queryset.filter(stock=0)
        return queryset


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'category', 'stock', 'stock_threshold', 'is_low_stock_display']
    list_filter = ['category', 'label', LowStockFilter]
    list_editable = ['stock', 'stock_threshold']
    search_fields = ['title', 'description']
    list_per_page = 20

    def is_low_stock_display(self, obj):
        if obj.stock <= 0:
            return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">缺货</span>')
        elif obj.is_low_stock():
            return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">预警</span>')
        return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px;">正常</span>')
    is_low_stock_display.short_description = '库存状态'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity', 'ordered']
    list_filter = ['ordered']
    search_fields = ['user__username', 'item__title']


from django.db import models

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)


admin.site.site_header = '电商管理后台'
admin.site.site_title = '电商管理后台'
admin.site.index_title = '欢迎使用电商管理后台'
