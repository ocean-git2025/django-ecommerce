from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Item, Order, OrderItem, Address, Payment, Coupon, Refund
import json
import os
import django

class FrontendFunctionalityTest(TestCase):
    """测试前端功能"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # 创建管理员用户
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        
        # 创建测试商品
        self.item = Item.objects.create(
            title='测试商品',
            price=10.0,
            category='S',
            label='P',
            slug='test-product',
            description='测试商品描述',
            stock=10,
            stock_threshold=5
        )
        
        # 创建测试订单
        self.order = Order.objects.create(
            ref_code='TEST123',
            user=self.user,
            ordered_date=django.utils.timezone.now(),
            status='P'  # 待处理状态
        )
    
    def test_frontend_pages(self):
        """测试前端页面加载"""
        print("=== 测试前端页面加载 ===")
        
        # 测试首页
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("✓ 首页加载成功")
        
        # 测试登录页面
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        print("✓ 登录页面加载成功")
        
        # 测试注册页面
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        print("✓ 注册页面加载成功")
        
        # 登录测试用户
        self.client.login(username='testuser', password='testpass123')
        print("✓ 用户登录成功")
        
        # 测试商品列表页
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        print("✓ 商品列表页加载成功")
        
        # 测试购物车页面
        response = self.client.get('/order/checkout/')
        self.assertEqual(response.status_code, 200)
        print("✓ 购物车页面加载成功")
        
        # 测试个人中心页面
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        print("✓ 个人中心页面加载成功")
        
        # 登录管理员用户
        self.client.login(username='admin', password='adminpass123')
        print("✓ 管理员登录成功")
        
        # 测试管理员仪表板
        response = self.client.get('/admin/dashboard/')
        self.assertEqual(response.status_code, 200)
        print("✓ 管理员仪表板加载成功")
        
        # 测试批量操作页面
        response = self.client.get('/admin/bulk-operations/')
        self.assertEqual(response.status_code, 200)
        print("✓ 批量操作页面加载成功")
    
    def test_api_endpoints(self):
        """测试API端点"""
        print("\n=== 测试API端点 ===")
        
        # 登录测试用户
        self.client.login(username='testuser', password='testpass123')
        
        # 测试库存查询API
        response = self.client.get(f'/api/stock/{self.item.slug}/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        print(f"✓ 库存查询API成功: {data}")
        
        # 测试订单状态查询API
        response = self.client.get(f'/api/order/{self.order.ref_code}/status/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        print(f"✓ 订单状态查询API成功: {data}")
        
        # 测试订单取消API
        response = self.client.post(
            f'/api/order/{self.order.ref_code}/status/update/',
            data=json.dumps({'status': 'X'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data.get('success'))
        print("✓ 订单取消API成功")
        
        # 检查库存是否恢复
        self.item.refresh_from_db()
        print(f"✓ 库存已恢复: 当前库存 {self.item.stock}")
    
    def test_javascript_files(self):
        """测试JavaScript文件是否存在"""
        print("\n=== 测试JavaScript文件 ===")
        
        js_files = [
            'static/js/stock_order_manager.js',
            'static/js/main.js',
        ]
        
        for js_file in js_files:
            # 使用绝对路径
            abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), js_file)
            self.assertTrue(os.path.exists(abs_path), f"文件不存在: {abs_path}")
            print(f"✓ {js_file} 存在")
    
    def test_template_files(self):
        """测试模板文件是否存在"""
        print("\n=== 测试模板文件 ===")
        
        template_files = [
            'templates/home.html',
            'templates/product_list.html',
            'templates/product_detail.html',
            'templates/order_summary.html',
            'templates/profile.html',
            'templates/admin/dashboard.html',
            'templates/admin/bulk_operations.html',
        ]
        
        for template_file in template_files:
            # 使用绝对路径
            abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), template_file)
            self.assertTrue(os.path.exists(abs_path), f"文件不存在: {abs_path}")
            print(f"✓ {template_file} 存在")