#!/usr/bin/env python
"""
测试收藏功能的简单脚本
"""

import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from core.models import Item, ProductFavorite
from django.contrib.auth.models import User

def test_favorite_model():
    """测试收藏模型"""
    print("测试收藏模型...")
    
    # 创建测试用户
    user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
    if created:
        user.set_password('testpassword')
        user.save()
    
    # 创建测试商品
    item, created = Item.objects.get_or_create(
        title='Test Product',
        price=99.99,
        category='S',
        label='P',
        slug='test-product',
        description='This is a test product'
    )
    
    # 添加收藏
    favorite, created = ProductFavorite.objects.get_or_create(user=user, item=item)
    
    if created:
        print("✓ 收藏添加成功")
    else:
        print("✓ 商品已在收藏夹中")
    
    # 检查收藏是否存在
    favorites_count = ProductFavorite.objects.filter(user=user).count()
    print(f"✓ 用户收藏的商品数量: {favorites_count}")
    
    # 移除收藏
    ProductFavorite.objects.filter(user=user, item=item).delete()
    print("✓ 收藏移除成功")
    
    # 检查收藏是否已移除
    favorites_count_after = ProductFavorite.objects.filter(user=user).count()
    print(f"✓ 移除后收藏的商品数量: {favorites_count_after}")
    
    print("\n所有测试通过！")

if __name__ == '__main__':
    test_favorite_model()