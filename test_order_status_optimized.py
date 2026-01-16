import os
import django
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from core.models import Order, Item, OrderItem
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test import Client

class TestOrderStatus(TestCase):
    def setUp(self):
        self.client = Client()
        # Get or create test user
        self.user, _ = get_user_model().objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        self.user.set_password('testpass123')
        self.user.save()
        self.client.login(username='testuser', password='testpass123')
        
        # Create a test item
        self.item = Item.objects.create(
            title='Test Item',
            price=10.99,
            category='C',
            label='P',
            description='Test description',
            stock=20,
            stock_threshold=10,
            slug='test-item'
        )
        
        # Create a test order with ordered_date
        self.order = Order.objects.create(
            user=self.user,
            ordered=False,
            status='P',  # Pending
            ordered_date=timezone.now()
        )
        
        # Add item to order
        OrderItem.objects.create(
            item=self.item,
            user=self.user,
            order=self.order,
            quantity=1,
            ordered=False
        )
        
        # Mark order as ordered
        self.order.ordered = True
        self.order.save()
        
        # Update order items to ordered
        self.order.items.update(ordered=True)
        
        print("\n" + "="*60)
        print("开始执行订单状态和库存预警功能测试")
        print("="*60)

    def test_order_status_initial(self):
        """Test that order status is initially pending"""
        print("\n1. 测试订单初始状态是否为待处理")
        print("-" * 40)
        self.assertEqual(self.order.status, 'P')
        print("✓ 订单状态正确：待处理")
        
    def test_order_cancellation(self):
        """Test that pending order can be cancelled"""
        print("\n2. 测试待处理订单是否可以取消")
        print("-" * 40)
        # Ensure order is pending
        self.order.status = 'P'
        self.order.save()
        
        response = self.client.post(reverse('core:cancel-order', kwargs={'order_id': self.order.id}))
        self.order.refresh_from_db()
        
        self.assertTrue(self.order.cancelled)
        print("✓ 待处理订单成功取消")
        
    def test_shipped_order_cancellation(self):
        """Test that shipped order cannot be cancelled"""
        print("\n3. 测试已发货订单是否无法取消")
        print("-" * 40)
        self.order.status = 'S'  # Shipped
        self.order.cancelled = False
        self.order.save()
        
        response = self.client.post(reverse('core:cancel-order', kwargs={'order_id': self.order.id}))
        self.order.refresh_from_db()
        
        self.assertFalse(self.order.cancelled)
        print("✓ 已发货订单确实无法取消")
        
    def test_low_stock_alert(self):
        """Test low stock alert functionality"""
        print("\n4. 测试库存预警功能")
        print("-" * 40)
        # Create item with low stock
        low_stock_item = Item.objects.create(
            title='Low Stock Item',
            price=19.99,
            category='C',
            label='S',
            description='Low stock test',
            stock=5,  # Below threshold of 10
            stock_threshold=10,
            slug='low-stock-item'
        )
        
        # Login as staff
        staff_user, _ = get_user_model().objects.get_or_create(
            username='staffuser',
            defaults={'email': 'staff@example.com', 'is_staff': True}
        )
        staff_user.set_password('staffpass123')
        staff_user.save()
        self.client.login(username='staffuser', password='staffpass123')
        
        response = self.client.get(reverse('core:low-stock-alert'))
        self.assertEqual(response.status_code, 200)
        
        items_in_response = list(response.context['items'])
        
        # Check if low stock item is in response
        low_stock_found = any(item.id == low_stock_item.id for item in items_in_response)
        self.assertTrue(low_stock_found)
        print(f"✓ 低库存商品 '{low_stock_item.title}' 被正确识别")
        
        # Check if normal stock item is not in response
        normal_stock_found = any(item.id == self.item.id for item in items_in_response)
        self.assertFalse(normal_stock_found)
        print(f"✓ 正常库存商品 '{self.item.title}' 未被错误标记")
        
    def test_order_status_update(self):
        """Test that order status can be updated"""
        print("\n5. 测试订单状态更新功能")
        print("-" * 40)
        
        # Test status update to Shipped
        self.order.status = 'S'
        self.order.save()
        self.assertEqual(self.order.status, 'S')
        print("✓ 订单状态成功更新为：已发货")
        
        # Test status update to Delivering
        self.order.status = 'D'
        self.order.save()
        self.assertEqual(self.order.status, 'D')
        print("✓ 订单状态成功更新为：配送中")
        
        # Test status update to Completed
        self.order.status = 'C'
        self.order.save()
        self.assertEqual(self.order.status, 'C')
        print("✓ 订单状态成功更新为：已完成")
        
    def test_order_detail_view(self):
        """Test that order detail view displays status correctly"""
        print("\n6. 测试订单详情页面状态显示")
        print("-" * 40)
        
        response = self.client.get(reverse('core:order-detail', kwargs={'pk': self.order.id}))
        self.assertEqual(response.status_code, 200)
        
        # Check if status choices are in context
        self.assertIn('status_choices', response.context)
        
        # Check if order status is displayed
        self.assertContains(response, self.order.get_status_display())
        print(f"✓ 订单详情页面正确显示状态：{self.order.get_status_display()}")
        
    def test_user_orders_view(self):
        """Test that user orders view displays user's orders"""
        print("\n7. 测试用户订单列表页面")
        print("-" * 40)
        
        response = self.client.get(reverse('core:user-orders'))
        self.assertEqual(response.status_code, 200)
        
        # Check if order is in context
        self.assertIn('orders', response.context)
        orders_in_context = list(response.context['orders'])
        self.assertIn(self.order, orders_in_context)
        print("✓ 用户订单列表正确显示用户的订单")

if __name__ == '__main__':
    # Run tests
    test = TestOrderStatus()
    test.setUp()
    
    test.test_order_status_initial()
    test.test_order_cancellation()
    test.test_shipped_order_cancellation()
    test.test_low_stock_alert()
    test.test_order_status_update()
    test.test_order_detail_view()
    test.test_user_orders_view()
    
    print("\n" + "="*60)
    print("✅ 所有测试通过！功能运行正常")
    print("="*60)
