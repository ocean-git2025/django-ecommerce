import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from core.models import Order, Item
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test import Client

class TestOrderStatus(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Create a test item
        self.item = Item.objects.create(
            title='Test Item',
            price=10.99,
            category='C',
            label='P',
            description='Test description',
            stock=20,
            stock_threshold=10
        )
        
        # Create a test order
        self.order = Order.objects.create(
            user=self.user,
            ordered=False,
            status='P'  # Pending
        )
        self.order.items.create(item=self.item, quantity=1, user=self.user)
        
    def test_order_status_initial(self):
        """Test that order status is initially pending"""
        self.assertEqual(self.order.status, 'P')
        print("✓ Order status is initially pending")
        
    def test_order_cancellation(self):
        """Test that pending order can be cancelled"""
        response = self.client.post(reverse('core:cancel-order', kwargs={'order_id': self.order.id}))
        self.order.refresh_from_db()
        self.assertTrue(self.order.cancelled)
        print("✓ Pending order can be cancelled")
        
    def test_shipped_order_cancellation(self):
        """Test that shipped order cannot be cancelled"""
        self.order.status = 'S'  # Shipped
        self.order.save()
        
        response = self.client.post(reverse('core:cancel-order', kwargs={'order_id': self.order.id}))
        self.order.refresh_from_db()
        self.assertFalse(self.order.cancelled)
        print("✓ Shipped order cannot be cancelled")
        
    def test_low_stock_alert(self):
        """Test low stock alert functionality"""
        # Create item with low stock
        low_stock_item = Item.objects.create(
            title='Low Stock Item',
            price=19.99,
            category='C',
            label='S',
            description='Low stock test',
            stock=5,  # Below threshold of 10
            stock_threshold=10
        )
        
        # Login as staff
        staff_user = get_user_model().objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        self.client.login(username='staffuser', password='staffpass123')
        
        response = self.client.get(reverse('core:low-stock-alert'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(low_stock_item, response.context['items'])
        self.assertNotIn(self.item, response.context['items'])  # Not low stock
        print("✓ Low stock alert works correctly")
        
    def test_order_status_update(self):
        """Test that order status can be updated"""
        self.order.status = 'S'  # Shipped
        self.order.save()
        self.assertEqual(self.order.status, 'S')
        
        self.order.status = 'D'  # Delivering
        self.order.save()
        self.assertEqual(self.order.status, 'D')
        
        self.order.status = 'C'  # Completed
        self.order.save()
        self.assertEqual(self.order.status, 'C')
        print("✓ Order status can be updated correctly")

if __name__ == '__main__':
    # Run tests
    test = TestOrderStatus()
    test.setUp()
    
    test.test_order_status_initial()
    test.test_order_cancellation()
    test.test_shipped_order_cancellation()
    test.test_low_stock_alert()
    test.test_order_status_update()
    
    print("\n✅ All tests passed!")