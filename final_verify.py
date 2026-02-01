#!/usr/bin/env python
"""
简单的前端功能验证脚本
"""

import os
import sys

def check_files():
    """检查关键文件是否存在"""
    print("=== 检查关键文件是否存在 ===")
    
    # 检查JavaScript文件
    js_files = [
        'static_in_env/js/stock_order_manager.js',
        'static_in_env/js/main.js',
    ]
    
    for js_file in js_files:
        if os.path.exists(js_file):
            print(f"✓ {js_file} 存在")
        else:
            print(f"✗ {js_file} 不存在")
    
    # 检查模板文件
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
    
    # 检查API视图文件
    if os.path.exists('core/api_views.py'):
        print("✓ core/api_views.py 存在")
    else:
        print("✗ core/api_views.py 不存在")

def check_url_config():
    """检查URL配置"""
    print("\n=== 检查URL配置 ===")
    
    # 检查core/urls.py
    if os.path.exists('core/urls.py'):
        print("✓ core/urls.py 存在")
        with open('core/urls.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'api/stock' in content:
                print("✓ 库存查询API URL配置存在")
            else:
                print("✗ 库存查询API URL配置不存在")
            
            if 'api/order' in content:
                print("✓ 订单API URL配置存在")
            else:
                print("✗ 订单API URL配置不存在")
    else:
        print("✗ core/urls.py 不存在")

def check_model_config():
    """检查模型配置"""
    print("\n=== 检查模型配置 ===")
    
    if os.path.exists('core/models.py'):
        print("✓ core/models.py 存在")
        with open('core/models.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'ORDER_STATUS_CHOICES' in content:
                print("✓ 订单状态配置存在")
            else:
                print("✗ 订单状态配置不存在")
            
            if 'stock_threshold' in content:
                print("✓ 库存阈值配置存在")
            else:
                print("✗ 库存阈值配置不存在")
    else:
        print("✗ core/models.py 不存在")

def check_admin_config():
    """检查管理员配置"""
    print("\n=== 检查管理员配置 ===")
    
    if os.path.exists('core/admin.py'):
        print("✓ core/admin.py 存在")
        with open('core/admin.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'dashboard' in content:
                print("✓ 管理员仪表板配置存在")
            else:
                print("✗ 管理员仪表板配置不存在")
            
            if 'bulk_operations' in content:
                print("✓ 批量操作配置存在")
            else:
                print("✗ 批量操作配置不存在")
    else:
        print("✗ core/admin.py 不存在")

if __name__ == '__main__':
    check_files()
    check_url_config()
    check_model_config()
    check_admin_config()
    print("\n=== 前端功能验证完成 ===")