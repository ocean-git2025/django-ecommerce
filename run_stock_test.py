import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from core.models import Item, Order
from django.contrib.auth.models import User
from django.db.models import F

print("=" * 60)
print("测试库存低于阈值时是否自动标记低库存")
print("=" * 60)

# 创建测试商品
print("\n1. 创建测试商品...")
item1 = Item.objects.create(
    title="测试商品1 - 低库存",
    price=99.99,
    category="S",
    label="P",
    slug="test-item-1",
    description="这是一个测试商品，库存低于阈值",
    stock=5,
    stock_threshold=10
)

item2 = Item.objects.create(
    title="测试商品2 - 正常库存",
    price=199.99,
    category="SW",
    label="S",
    slug="test-item-2",
    description="这是一个测试商品，库存正常",
    stock=20,
    stock_threshold=10
)

item3 = Item.objects.create(
    title="测试商品3 - 刚好等于阈值",
    price=149.99,
    category="OW",
    label="D",
    slug="test-item-3",
    description="这是一个测试商品，库存刚好等于阈值",
    stock=10,
    stock_threshold=10
)

print(f"✓ 创建了3个测试商品")

# 测试is_low_stock()方法
print("\n2. 测试is_low_stock()方法...")
print(f"商品1: {item1.title}")
print(f"  库存: {item1.stock}, 阈值: {item1.stock_threshold}")
print(f"  is_low_stock(): {item1.is_low_stock()}")
print(f"  预期结果: True (5 <= 10)")
print(f"  测试结果: {'✓ 通过' if item1.is_low_stock() == True else '✗ 失败'}")

print(f"\n商品2: {item2.title}")
print(f"  库存: {item2.stock}, 阈值: {item2.stock_threshold}")
print(f"  is_low_stock(): {item2.is_low_stock()}")
print(f"  预期结果: False (20 > 10)")
print(f"  测试结果: {'✓ 通过' if item2.is_low_stock() == False else '✗ 失败'}")

print(f"\n商品3: {item3.title}")
print(f"  库存: {item3.stock}, 阈值: {item3.stock_threshold}")
print(f"  is_low_stock(): {item3.is_low_stock()}")
print(f"  预期结果: True (10 <= 10)")
print(f"  测试结果: {'✓ 通过' if item3.is_low_stock() == True else '✗ 失败'}")

# 测试查询低库存商品
print("\n3. 测试查询低库存商品...")
low_stock_items = Item.objects.filter(stock__lte=F('stock_threshold'))
print(f"查询到 {low_stock_items.count()} 个低库存商品:")
for item in low_stock_items:
    print(f"  - {item.title} (库存: {item.stock}, 阈值: {item.stock_threshold})")

# 测试订单状态
print("\n4. 测试订单状态...")
user = User.objects.first()
if user:
    order = Order.objects.create(
        user=user,
        ordered_date="2026-01-17 12:00:00",
        ordered=True,
        status='P'
    )
    print(f"✓ 创建测试订单")
    print(f"  订单状态: {order.get_status_display()}")
    print(f"  can_cancel(): {order.can_cancel()}")
    print(f"  预期结果: True (状态为P)")
    print(f"  测试结果: {'✓ 通过' if order.can_cancel() == True else '✗ 失败'}")
    
    # 测试取消订单
    order.status = 'X'
    order.save()
    print(f"\n  取消订单后状态: {order.get_status_display()}")
    print(f"  can_cancel(): {order.can_cancel()}")
    print(f"  预期结果: False (状态为X)")
    print(f"  测试结果: {'✓ 通过' if order.can_cancel() == False else '✗ 失败'}")
else:
    print("  ⚠ 没有找到用户，跳过订单测试")

# 清理测试数据
print("\n5. 清理测试数据...")
item1.delete()
item2.delete()
item3.delete()
if user:
    order.delete()
print("✓ 清理完成")

print("\n" + "=" * 60)
print("所有测试完成！")
print("=" * 60)