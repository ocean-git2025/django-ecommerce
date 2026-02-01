from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    OrderDetailView,
    cancel_order,
    OrderHistoryView,
    ProfileView
)
from . import api_views

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('order/<ref_code>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/<ref_code>/cancel/', cancel_order, name='cancel-order'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # API端点
    path('api/stock/<int:item_id>/', api_views.check_stock, name='api-check-stock'),
    path('api/stocks/', api_views.check_multiple_stocks, name='api-check-stocks'),
    path('api/low-stock-items/', api_views.get_low_stock_items, name='api-low-stock-items'),
    path('api/order/<str:order_ref_code>/status/', api_views.get_order_status, name='api-order-status'),
    path('api/orders/', api_views.get_user_orders, name='api-user-orders'),
    path('api/order/<str:order_ref_code>/status/update/', api_views.UpdateOrderStatusView.as_view(), name='api-update-order-status'),
    path('api/stock/<int:item_id>/update/', api_views.UpdateStockView.as_view(), name='api-update-stock'),
]
