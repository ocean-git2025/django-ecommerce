#!/usr/bin/env python
"""
简单的订单取消测试
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

def simple_test():
    """简单测试"""
    print("=== 简单订单取消测试 ===")
    
    # 创建测试用户
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print("✓ 创建测试用户")
    else:
        print("✓ 使用现有测试用户")
    
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
        print("✓ 创建测试订单")
    else:
        print("✓ 使用现有测试订单")
    
    # 创建客户端并登录
    client = Client()
    client.login(username='testuser', password='testpass123')
    
    # 测试直接调用视图函数
    from core.api_views import UpdateOrderStatusView
    
    view = UpdateOrderStatusView()
    request = client.post('/api/order/TEST123/status/update/', 
                         data=json.dumps({'status': 'X'}),
                         content_type='application/json')
    
    # 检查订单状态
    order.refresh_from_db()
    print(f"当前订单状态: {order.status} - {order.get_status_display()}")
    
    return True

if __name__ == '__main__':
    simple_test()