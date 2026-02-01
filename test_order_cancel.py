#!/usr/bin/env python
"""
测试订单取消和状态更新功能
"""

import os
import sys
import django

# 设置Django环境
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Order, OrderItem, Item
import json

def test_order_cancel():
    """测试订单取消功能"""
    print("=== 测试订单取消功能 ===")
    
    # 创建测试用户
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print("✓ 创建测试用户")
    else:
        print("✓ 使用现有测试用户")
    
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
    
    if created:
        print("✓ 创建测试商品")
    else:
        print("✓ 使用现有测试商品")
    
    # 创建测试订单
    order, created = Order.objects.get_or_create(
        ref_code='TEST123',
        user=user,
        defaults={
            'ordered_date': django.utils.timezone.now(),
            'status': 'P'  # 待处理状态
        }
    )
    
    if created:
        # 创建订单项
        OrderItem.objects.get_or_create(
            user=user,
            ordered=True,
            item=item,
            order=order,
            defaults={'quantity': 2}
        )
        print("✓ 创建测试订单")
    else:
        print("✓ 使用现有测试订单")
    
    # 创建客户端并登录
    client = Client()
    client.login(username='testuser', password='testpass123')
    
    # 测试获取订单状态
    response = client.get('/api/order/TEST123/status/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 获取订单状态成功: {data['status_display']}")
    else:
        print(f"✗ 获取订单状态失败: {response.status_code}")
        return False
    
    # 测试取消订单
    response = client.post(
        '/api/order/TEST123/status/update/',
        data=json.dumps({'status': 'X'}),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print("✓ 订单取消成功")
            # 检查库存是否恢复
            item.refresh_from_db()
            print(f"✓ 库存已恢复: 当前库存 {item.stock}")
        else:
            print(f"✗ 订单取消失败: {data.get('error', '未知错误')}")
    else:
        print(f"✗ 订单取消请求失败: {response.status_code}")
    
    # 测试再次获取订单状态
    response = client.get('/api/order/TEST123/status/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 取消后订单状态: {data['status_display']}")
    else:
        print(f"✗ 获取取消后订单状态失败: {response.status_code}")
    
    return True

if __name__ == '__main__':
    test_order_cancel()