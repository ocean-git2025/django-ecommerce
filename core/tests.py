from django.test import TestCase, Client
from django.urls import reverse
from .models import Item, CATEGORY_CHOICES


class ItemModelTests(TestCase):
    """Item模型测试"""

    def test_category_choices(self):
        """测试分类选项是否正确"""
        expected_choices = (
            ('CLOTHING', '服装'),
            ('ACCESSORY', '配饰'),
            ('DIGITAL', '数码'),
        )
        self.assertEqual(CATEGORY_CHOICES, expected_choices)

    def test_item_category_max_length(self):
        """测试category字段最大长度"""
        item = Item(
            title='Test Item',
            price=100.0,
            category='CLOTHING',
            label='P',
            slug='test-item',
            description='Test description'
        )
        max_length = item._meta.get_field('category').max_length
        self.assertEqual(max_length, 10)


class HomeViewTests(TestCase):
    """HomeView视图测试"""

    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        """测试首页返回状态码"""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """测试首页使用正确模板"""
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_context_category_default(self):
        """测试默认分类上下文"""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.context['current_category'], 'all')


class CategoryFilterTests(TestCase):
    """分类筛选功能测试"""

    def setUp(self):
        self.client = Client()

    def test_filter_by_clothing_category(self):
        """测试服装分类筛选"""
        response = self.client.get(reverse('core:home') + '?category=CLOTHING')
        self.assertEqual(response.context['current_category'], 'CLOTHING')

    def test_filter_by_accessory_category(self):
        """测试配饰分类筛选"""
        response = self.client.get(reverse('core:home') + '?category=ACCESSORY')
        self.assertEqual(response.context['current_category'], 'ACCESSORY')

    def test_filter_by_digital_category(self):
        """测试数码分类筛选"""
        response = self.client.get(reverse('core:home') + '?category=DIGITAL')
        self.assertEqual(response.context['current_category'], 'DIGITAL')

    def test_filter_all_categories(self):
        """测试全部分类"""
        response = self.client.get(reverse('core:home') + '?category=all')
        self.assertEqual(response.context['current_category'], 'all')
