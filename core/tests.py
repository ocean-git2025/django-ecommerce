from django.test import TestCase, Client
from django.urls import reverse
from core.models import Item


class CategoryFilterTest(TestCase):
    def setUp(self):
        # 创建测试数据
        self.item1 = Item.objects.create(
            title="服装商品",
            price=100.0,
            category="C",
            slug="clothing-item",
            description="这是一个服装商品",
            image=""
        )
        self.item2 = Item.objects.create(
            title="配饰商品",
            price=50.0,
            category="A",
            slug="accessory-item",
            description="这是一个配饰商品",
            image=""
        )
        self.item3 = Item.objects.create(
            title="数码商品",
            price=200.0,
            category="D",
            slug="digital-item",
            description="这是一个数码商品",
            image=""
        )
    
    def test_home_view_without_filter(self):
        """测试首页不筛选时显示所有商品"""
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "服装商品")
        self.assertContains(response, "配饰商品")
        self.assertContains(response, "数码商品")
    
    def test_home_view_with_clothing_filter(self):
        """测试筛选服装分类"""
        client = Client()
        response = client.get(reverse('core:home') + "?category=C")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "服装商品")
        self.assertNotContains(response, "配饰商品")
        self.assertNotContains(response, "数码商品")
    
    def test_home_view_with_accessory_filter(self):
        """测试筛选配饰分类"""
        client = Client()
        response = client.get(reverse('core:home') + "?category=A")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "服装商品")
        self.assertContains(response, "配饰商品")
        self.assertNotContains(response, "数码商品")
    
    def test_home_view_with_digital_filter(self):
        """测试筛选数码分类"""
        client = Client()
        response = client.get(reverse('core:home') + "?category=D")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "服装商品")
        self.assertNotContains(response, "配饰商品")
        self.assertContains(response, "数码商品")