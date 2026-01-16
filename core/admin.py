from django.contrib import admin
from django.db.models import F
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


def set_order_pending(modeladmin, request, queryset):
    queryset.update(status='P')


set_order_pending.short_description = 'Set status to Pending'


def set_order_shipped(modeladmin, request, queryset):
    queryset.update(status='S')


set_order_shipped.short_description = 'Set status to Shipped'


def set_order_delivering(modeladmin, request, queryset):
    queryset.update(status='D')


set_order_delivering.short_description = 'Set status to Delivering'


def set_order_completed(modeladmin, request, queryset):
    queryset.update(status='C')


set_order_completed.short_description = 'Set status to Completed'


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'category', 'label', 'stock', 'stock_threshold', 'is_low_stock']
    list_filter = ['category', 'label', 'stock_threshold']
    search_fields = ['title', 'description']
    
    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ref_code', 'ordered', 'status', 'being_delivered', 'received', 
                    'refund_requested', 'refund_granted', 'shipping_address', 'billing_address',
                    'payment', 'coupon', 'get_total']
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered', 'status', 'being_delivered', 'received', 'refund_requested', 'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted, set_order_pending, set_order_shipped, set_order_delivering, set_order_completed]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'payment', 'coupon')


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


class LowStockItemsAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'stock_threshold']
    list_filter = ['category', 'label']
    search_fields = ['title', 'description']
    change_list_template = 'admin/low_stock_items_change_list.html'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(stock__lte=F('stock_threshold'))
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        low_stock_count = Item.objects.filter(stock__lte=F('stock_threshold')).count()
        extra_context['low_stock_count'] = low_stock_count
        return super().changelist_view(request, extra_context)


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)


class MyAdminSite(AdminSite):
    site_header = 'DJe-commerce Administration'
    site_title = 'DJe-commerce Admin Portal'
    index_title = 'Welcome to DJe-commerce Admin Portal'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('low-stock-items/', self.admin_view(self.low_stock_items_view), name='low-stock-items'),
        ]
        return custom_urls + urls

    def low_stock_items_view(self, request):
        from django.shortcuts import render
        low_stock_items = Item.objects.filter(stock__lte=F('stock_threshold'))
        context = {
            'title': 'Low Stock Items',
            'low_stock_items': low_stock_items,
            'opts': Item._meta,
            'has_change_permission': self.has_change_permission(request),
        }
        return render(request, 'admin/low_stock_items_dashboard.html', context)

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        low_stock_count = Item.objects.filter(stock__lte=F('stock_threshold')).count()
        extra_context['low_stock_count'] = low_stock_count
        return super().index(request, extra_context)


my_admin_site = MyAdminSite(name='myadmin')
my_admin_site.register(Item, ItemAdmin)
my_admin_site.register(OrderItem)
my_admin_site.register(Order, OrderAdmin)
my_admin_site.register(Payment)
my_admin_site.register(Coupon)
my_admin_site.register(Refund)
my_admin_site.register(Address, AddressAdmin)
my_admin_site.register(UserProfile)