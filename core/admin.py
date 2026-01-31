from django.contrib import admin
from django.utils.html import format_html

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


def make_status_pending(modeladmin, request, queryset):
    queryset.update(status='PENDING')


make_status_pending.short_description = '批量设置为待处理'


def make_status_shipped(modeladmin, request, queryset):
    queryset.update(status='SHIPPED')


make_status_shipped.short_description = '批量设置为已发货'


def make_status_delivering(modeladmin, request, queryset):
    queryset.update(status='DELIVERING')


make_status_delivering.short_description = '批量设置为配送中'


def make_status_completed(modeladmin, request, queryset):
    queryset.update(status='COMPLETED')


make_status_completed.short_description = '批量设置为已完成'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['ref_code',
                    'user',
                    'ordered',
                    'status',
                    'ordered_date',
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
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted, make_status_pending, make_status_shipped, make_status_delivering, make_status_completed]
    list_editable = ['status']


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
    list_display = ['title', 'price', 'stock', 'stock_threshold', 'stock_status']
    list_filter = ['category', 'label']
    search_fields = ['title', 'description']
    list_editable = ['stock', 'stock_threshold']

    def stock_status(self, obj):
        if obj.stock <= obj.stock_threshold:
            return format_html('<span style="color: red; font-weight: bold;">库存不足</span>')
        return format_html('<span style="color: green;">库存正常</span>')
    
    stock_status.short_description = '库存状态'


class LowStockItem(Item):
    class Meta:
        proxy = True
        verbose_name = '库存预警商品'
        verbose_name_plural = '库存预警商品'


class LowStockItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'stock_threshold', 'stock_warning']
    list_filter = ['category', 'label']
    search_fields = ['title', 'description']
    list_editable = ['stock', 'stock_threshold']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(stock__lte=models.F('stock_threshold'))

    def stock_warning(self, obj):
        return format_html('<span style="color: red; font-weight: bold;">⚠️ 库存低于阈值</span>')
    
    stock_warning.short_description = '预警状态'

    def has_add_permission(self, request):
        return False


from django.db import models

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(LowStockItem, LowStockItemAdmin)
