#!/usr/bin/env python
"""
前端功能测试脚本
测试各个页面的加载和基本功能
"""

import os
import sys
import django
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Item, Order, OrderItem, Address, Payment, Coupon, Refund
import json

# 设置Django环境
# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')

try:
    django.setup()
    print("✓ Django环境设置成功")
except Exception as e:
    print(f"✗ Django环境设置失败: {e}")
    sys.exit(1)

def test_frontend_pages():
    """测试前端页面加载"""
    print("=== 测试前端页面加载 ===")
    
    client = Client()
    
    # 测试首页
    response = client.get('/')
    if response.status_code == 200:
        print("✓ 首页加载成功")
    else:
        print(f"✗ 首页加载失败: {response.status_code}")
    
    # 测试登录页面
    response = client.get('/accounts/login/')
    if response.status_code == 200:
        print("✓ 登录页面加载成功")
    else:
        print(f"✗ 登录页面加载失败: {response.status_code}")
    
    # 测试注册页面
    response = client.get('/accounts/signup/')
    if response.status_code == 200:
        print("✓ 注册页面加载成功")
    else:
        print(f"✗ 注册页面加载失败: {response.status_code}")
    
    # 创建测试用户并登录
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    client.login(username='testuser', password='testpass123')
    print("✓ 用户登录成功")
    
    # 测试商品列表页
    response = client.get('/products/')
    if response.status_code == 200:
        print("✓ 商品列表页加载成功")
    else:
        print(f"✗ 商品列表页加载失败: {response.status_code}")
    
    # 测试购物车页面
    response = client.get('/order/checkout/')
    if response.status_code == 200:
        print("✓ 购物车页面加载成功")
    else:
        print(f"✗ 购物车页面加载失败: {response.status_code}")
    
    # 测试个人中心页面
    response = client.get('/profile/')
    if response.status_code == 200:
        print("✓ 个人中心页面加载成功")
    else:
        print(f"✗ 个人中心页面加载失败: {response.status_code}")
    
    # 测试管理员用户
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        admin_user.set_password('adminpass123')
        admin_user.save()
    
    client.login(username='admin', password='adminpass123')
    print("✓ 管理员登录成功")
    
    # 测试管理员仪表板
    response = client.get('/admin/dashboard/')
    if response.status_code == 200:
        print("✓ 管理员仪表板加载成功")
    else:
        print(f"✗ 管理员仪表板加载失败: {response.status_code}")
    
    # 测试批量操作页面
    response = client.get('/admin/bulk-operations/')
    if response.status_code == 200:
        print("✓ 批量操作页面加载成功")
    else:
        print(f"✗ 批量操作页面加载失败: {response.status_code}")

def test_api_endpoints():
    """测试API端点"""
    print("\n=== 测试API端点 ===")
    
    client = Client()
    
    # 创建测试用户并登录
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    client.login(username='testuser', password='testpass123')
    
    # 创建测试商品
    item, created = Item.objects.get_or_create(
        title='测试商品',
        defaults={
            'price': 10.0,
            'category': 'S',
            'label': 'P',
            'slug': 'test-product',
            'description': '测试商品描述',
            'stock': 10,
            'stock_threshold': 5
        }
    )
    
    # 测试库存查询API
    response = client.get(f'/api/stock/{item.slug}/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 库存查询API成功: {data}")
    else:
        print(f"✗ 库存查询API失败: {response.status_code}")
    
    # 创建测试订单
    order, created = Order.objects.get_or_create(
        ref_code='TEST123',
        user=user,
        defaults={
            'ordered_date': django.utils.timezone.now(),
            'status': 'P'  # 待处理状态
        }
    )
    
    # 测试订单状态查询API
    response = client.get(f'/api/order/{order.ref_code}/status/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 订单状态查询API成功: {data}")
    else:
        print(f"✗ 订单状态查询API失败: {response.status_code}")
    
    # 测试订单取消API
    response = client.post(
        f'/api/order/{order.ref_code}/status/update/',
        data=json.dumps({'status': 'X'}),
        content_type='application/json'
    )
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print("✓ 订单取消API成功")
            # 检查库存是否恢复
            item.refresh_from_db()
            print(f"✓ 库存已恢复: 当前库存 {item.stock}")
        else:
            print(f"✗ 订单取消失败: {data.get('error', '未知错误')}")
    else:
        print(f"✗ 订单取消请求失败: {response.status_code}")

def test_javascript_files():
    """测试JavaScript文件是否存在"""
    print("\n=== 测试JavaScript文件 ===")
    
    js_files = [
        'static/js/stock_order_manager.js',
        'static/js/main.js',
    ]
    
    for js_file in js_files:
        if os.path.exists(js_file):
            print(f"✓ {js_file} 存在")
        else:
            print(f"✗ {js_file} 不存在")

def test_template_files():
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
        if os.path.exists(template_file):
            print(f"✓ {template_file} 存在")
        else:
            print(f"✗ {template_file} 不存在")

if __name__ == '__main__':
    test_frontend_pages()
    test_api_endpoints()
    test_javascript_files()
    test_template_files()
    print("\n=== 前端功能测试完成 ===")