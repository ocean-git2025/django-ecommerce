#!/usr/bin/env python
"""
简化的API测试脚本
"""

import requests
import json

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://127.0.0.1:8000"
    
    print("=== 测试API端点 ===")
    
    # 测试商品列表页
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✓ 商品列表页加载成功")
            if 'data-item-id' in response.text:
                print("✓ 商品列表页包含数据属性")
            else:
                print("✗ 商品列表页缺少数据属性")
        else:
            print(f"✗ 商品列表页加载失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 连接服务器失败: {str(e)}")
        return False
    
    # 测试库存API
    try:
        response = requests.get(f"{base_url}/api/stock/1/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 库存API测试成功: 商品ID 1 - 库存: {data.get('stock', 'N/A')}")
        else:
            print(f"✗ 库存API测试失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 库存API测试出错: {str(e)}")
    
    # 测试低库存API
    try:
        response = requests.get(f"{base_url}/api/low-stock-items/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 低库存API测试成功: 找到 {data.get('count', 0)} 个低库存商品")
        else:
            print(f"✗ 低库存API测试失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 低库存API测试出错: {str(e)}")
    
    return True

if __name__ == '__main__':
    test_api_endpoints()