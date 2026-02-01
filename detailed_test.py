#!/usr/bin/env python
"""
详细的订单取消测试
"""

import os
import sys
import django

# 设置Django环境
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.auth.models import User
from core.models import Order, OrderItem, Item
from core.api_views import UpdateOrderStatusView
import json

def detailed_test():
    """详细测试"""
    print("=== 详细订单取消测试 ===")
    
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
    
    # 创建RequestFactory
    factory = RequestFactory()
    
    # 创建POST请求
    request = factory.post(
        '/api/order/TEST123/status/update/',
        data=json.dumps({'status': 'X'}),
        content_type='application/json'
    )
    
    # 设置用户
    request.user = user
    
    # 创建视图实例
    view = UpdateOrderStatusView()
    
    try:
        # 调用视图方法
        response = view.post(request, 'TEST123')
        print(f"响应状态码: {response.status_code}")
        
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            print(f"响应内容: {content}")
    except Exception as e:
        print(f"异常: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 检查订单状态
    order.refresh_from_db()
    print(f"当前订单状态: {order.status} - {order.get_status_display()}")
    
    return True

if __name__ == '__main__':
    detailed_test()