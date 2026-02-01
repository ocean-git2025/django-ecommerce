#!/usr/bin/env python
"""
测试前后端交互功能的脚本
测试库存查询和订单状态API
"""

import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Item, Order, OrderItem
import json

def test_stock_api():
    """测试库存API"""
    print("=== 测试库存API ===")
    
    client = Client()
    
    # 获取所有商品
    items = Item.objects.all()
    if not items:
        print("没有找到商品，请先创建一些商品")
        return False
    
    # 测试单个商品库存查询
    item = items[0]
    response = client.get(f'/api/stock/{item.id}/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 单个商品库存查询成功: {data['title']} - 库存: {data['stock']}")
    else:
        print(f"✗ 单个商品库存查询失败: {response.status_code}")
        return False
    
    # 测试多个商品库存查询
    item_ids = [item.id for item in items[:3]]
    response = client.get(f'/api/stocks/?ids={",".join(map(str, item_ids))}/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 多个商品库存查询成功: 查询了 {len(data['items'])} 个商品")
    else:
        print(f"✗ 多个商品库存查询失败: {response.status_code}")
        return False
    
    # 测试低库存商品查询
    response = client.get('/api/low-stock-items/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 低库存商品查询成功: 找到 {data['count']} 个低库存商品")
    else:
        print(f"✗ 低库存商品查询失败: {response.status_code}")
        return False
    
    return True

def test_order_api():
    """测试订单API"""
    print("\n=== 测试订单API ===")
    
    # 创建测试用户
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print("创建了测试用户")
    
    client = Client()
    
    # 登录测试用户
    client.login(username='testuser', password='testpass123')
    
    # 获取用户的订单
    orders = Order.objects.filter(user=user, ordered=True)
    if not orders:
        print("没有找到订单，跳过订单API测试")
        return True
    
    # 测试获取用户所有订单
    response = client.get('/api/orders/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 获取用户订单成功: 找到 {len(data['orders'])} 个订单")
    else:
        print(f"✗ 获取用户订单失败: {response.status_code}")
        return False
    
    # 测试获取单个订单状态
    order = orders[0]
    response = client.get(f'/api/order/{order.ref_code}/status/')
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ 获取订单状态成功: {data['ref_code']} - 状态: {data['status_display']}")
    else:
        print(f"✗ 获取订单状态失败: {response.status_code}")
        return False
    
    return True

def test_frontend_integration():
    """测试前端集成"""
    print("\n=== 测试前端集成 ===")
    
    client = Client()
    
    # 测试商品列表页
    response = client.get('/')
    if response.status_code == 200:
        print("✓ 商品列表页加载成功")
        # 检查是否包含我们的数据属性
        if 'data-item-id' in response.content.decode():
            print("✓ 商品列表页包含数据属性")
        else:
            print("✗ 商品列表页缺少数据属性")
            return False
    else:
        print(f"✗ 商品列表页加载失败: {response.status_code}")
        return False
    
    # 测试商品详情页
    items = Item.objects.all()
    if items:
        item = items[0]
        response = client.get(f'/product/{item.slug}/')
        if response.status_code == 200:
            print("✓ 商品详情页加载成功")
            # 检查是否包含我们的数据属性
            if 'data-item-id' in response.content.decode():
                print("✓ 商品详情页包含数据属性")
            else:
                print("✗ 商品详情页缺少数据属性")
                return False
        else:
            print(f"✗ 商品详情页加载失败: {response.status_code}")
            return False
    
    return True

def main():
    """主测试函数"""
    print("开始测试前后端交互功能...")
    
    # 测试库存API
    stock_test_passed = test_stock_api()
    
    # 测试订单API
    order_test_passed = test_order_api()
    
    # 测试前端集成
    frontend_test_passed = test_frontend_integration()
    
    # 总结测试结果
    print("\n=== 测试结果总结 ===")
    if stock_test_passed and order_test_passed and frontend_test_passed:
        print("✓ 所有测试通过！前后端交互功能正常工作。")
        return True
    else:
        print("✗ 部分测试失败，请检查相关功能。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)