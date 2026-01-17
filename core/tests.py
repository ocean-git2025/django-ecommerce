from django.test import TestCase
from django.urls import reverse
from .models import Item

class ItemCategoryTest(TestCase):
    def setUp(self):
        self.item1 = Item.objects.create(
            title="测试服装",
            price=99.99,
            category="CL",
            label="P",
            slug="test-clothing",
            description="测试服装描述"
        )
        self.item2 = Item.objects.create(
            title="测试配饰",
            price=49.99,
            category="AC",
            label="S",
            slug="test-accessory",
            description="测试配饰描述"
        )
        self.item3 = Item.objects.create(
            title="测试数码产品",
            price=199.99,
            category="EL",
            label="D",
            slug="test-electronic",
            description="测试数码描述"
        )

    def test_category_filter(self):
        response = self.client.get(reverse('core:home'), {'category': 'CL'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['object_list'][0].title, "测试服装")

    def test_search_filter(self):
        response = self.client.get(reverse('core:home'), {'search': '数码'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['object_list'][0].title, "测试数码产品")

    def test_combined_filter(self):
        response = self.client.get(reverse('core:home'), {'category': 'EL', 'search': '测试'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertEqual(response.context['object_list'][0].title, "测试数码产品")

    def test_reset_filter(self):
        response = self.client.get(reverse('core:home'), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
