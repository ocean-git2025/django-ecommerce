from django.contrib import admin
from django.db.models import F

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, StockAlert


def make_shipped(modeladmin, request, queryset):
    queryset.update(status='S')


def make_delivering(modeladmin, request, queryset):
    queryset.update(status='D')


def make_completed(modeladmin, request, queryset):
    queryset.update(status='C')


make_shipped.short_description = '标记为已发货'
make_delivering.short_description = '标记为配送中'
make_completed.short_description = '标记为已完成'


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ref_code',
                    'ordered',
                    'status',
                    'ordered_date',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'cancelled'
                    ]
    list_display_links = [
        'user',
        'ref_code'
    ]
    list_filter = ['ordered',
                   'status',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted',
                   'cancelled']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted, make_shipped, make_delivering, make_completed]


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
    list_display = ['title', 'price', 'stock', 'stock_threshold', 'low_stock_warning', 'category', 'label']
    list_filter = ['category', 'label']
    search_fields = ['title', 'description']
    list_editable = ['stock', 'stock_threshold']

    def low_stock_warning(self, obj):
        if obj.stock <= obj.stock_threshold:
            return '<span style="color: red;">⚠️ 库存不足</span>'
        return ''
    low_stock_warning.allow_tags = True
    low_stock_warning.short_description = '库存预警'

    def changelist_view(self, request, extra_context=None):
        low_stock = Item.objects.filter(stock__lte=F('stock_threshold'))
        extra_context = extra_context or {}
        extra_context['low_stock_items'] = low_stock
        return super().changelist_view(request, extra_context)


class StockAlertAdmin(admin.ModelAdmin):
    list_display = ['item', 'current_stock', 'threshold', 'created_at', 'resolved']
    list_filter = ['resolved', 'created_at']
    search_fields = ['item__title']
    list_editable = ['resolved']


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(StockAlert, StockAlertAdmin)
