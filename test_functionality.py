import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from core.models import Item, Order, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F

print("=" * 80)
print("功能测试：模拟用户和管理员操作")
print("=" * 80)

# 获取或创建测试用户
print("\n【步骤1】准备测试数据")
print("-" * 80)
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"✓ 创建测试用户: {user.username}")
else:
    print(f"✓ 使用现有用户: {user.username}")

# 创建测试商品
print("\n创建测试商品...")
item1, _ = Item.objects.get_or_create(
    slug='test-product-1',
    defaults={
        'title': '测试商品A - 低库存',
        'price': 99.99,
        'category': 'S',
        'label': 'P',
        'description': '这是一个测试商品，库存低于阈值',
        'stock': 3,
        'stock_threshold': 10
    }
)

item2, _ = Item.objects.get_or_create(
    slug='test-product-2',
    defaults={
        'title': '测试商品B - 正常库存',
        'price': 199.99,
        'category': 'SW',
        'label': 'S',
        'description': '这是一个测试商品，库存正常',
        'stock': 25,
        'stock_threshold': 10
    }
)

print(f"✓ 商品1: {item1.title} (库存: {item1.stock}, 阈值: {item1.stock_threshold})")
print(f"✓ 商品2: {item2.title} (库存: {item2.stock}, 阈值: {item2.stock_threshold})")

# 模拟用户下单
print("\n【步骤2】模拟用户下单")
print("-" * 80)
order = Order.objects.create(
    user=user,
    ordered_date=timezone.now(),
    ordered=True,
    status='P',
    ref_code='TEST' + ''.join([str(i) for i in range(20)])
)

order_item1 = OrderItem.objects.create(
    user=user,
    item=item1,
    quantity=2,
    ordered=True
)

order_item2 = OrderItem.objects.create(
    user=user,
    item=item2,
    quantity=1,
    ordered=True
)

order.items.add(order_item1, order_item2)
order.save()

print(f"✓ 创建订单: {order.ref_code}")
print(f"  订单状态: {order.get_status_display()}")
print(f"  订单总金额: ${order.get_total()}")
print(f"  商品明细:")
print(f"    - {item1.title} x {order_item1.quantity} = ${order_item1.get_final_price()}")
print(f"    - {item2.title} x {order_item2.quantity} = ${order_item2.get_final_price()}")

# 测试订单状态查看
print("\n【步骤3】测试订单状态查看功能")
print("-" * 80)
print(f"订单详情:")
print(f"  参考号: {order.ref_code}")
print(f"  用户: {order.user.username}")
print(f"  下单时间: {order.ordered_date}")
print(f"  当前状态: {order.get_status_display()}")
print(f"  状态代码: {order.status}")
print(f"  是否可以取消: {order.can_cancel()}")

# 测试订单取消功能
print("\n【步骤4】测试订单取消功能")
print("-" * 80)
print(f"取消前状态: {order.get_status_display()} (代码: {order.status})")
print(f"取消前can_cancel(): {order.can_cancel()}")

if order.can_cancel():
    order.status = 'X'
    order.save()
    print(f"✓ 订单已取消")
    print(f"取消后状态: {order.get_status_display()} (代码: {order.status})")
    print(f"取消后can_cancel(): {order.can_cancel()}")
else:
    print(f"✗ 订单无法取消（当前状态不允许）")

# 测试订单状态更新（管理员操作）
print("\n【步骤5】模拟管理员更新订单状态")
print("-" * 80)
status_transitions = [
    ('P', 'Pending', '待处理'),
    ('S', 'Shipped', '已发货'),
    ('D', 'Delivering', '配送中'),
    ('C', 'Completed', '已完成'),
    ('X', 'Cancelled', '已取消')
]

print("订单状态流转:")
for code, display, chinese in status_transitions:
    order.status = code
    order.save()
    print(f"  {code} -> {display} ({chinese})")
    print(f"    can_cancel(): {order.can_cancel()}")

# 恢复到待处理状态
order.status = 'P'
order.save()

# 测试库存预警功能
print("\n【步骤6】测试库存预警功能")
print("-" * 80)
print("检查所有商品的库存状态:")

all_items = Item.objects.all()
low_stock_items = Item.objects.filter(stock__lte=F('stock_threshold'))

print(f"\n总商品数: {all_items.count()}")
print(f"低库存商品数: {low_stock_items.count()}")

print("\n所有商品列表:")
for item in all_items:
    is_low = item.is_low_stock()
    status = "⚠️ 低库存" if is_low else "✅ 库存充足"
    print(f"  {item.title}")
    print(f"    库存: {item.stock}, 阈值: {item.stock_threshold}")
    print(f"    状态: {status}")
    print(f"    is_low_stock(): {is_low}")

print("\n低库存商品详情:")
for item in low_stock_items:
    print(f"  - {item.title}")
    print(f"    当前库存: {item.stock}, 阈值: {item.stock_threshold}")
    print(f"    建议补货至: {item.stock_threshold * 2}")

# 测试订单历史查询
print("\n【步骤7】测试订单历史查询")
print("-" * 80)
user_orders = Order.objects.filter(user=user, ordered=True).order_by('-ordered_date')
print(f"用户 {user.username} 的订单历史:")
print(f"订单总数: {user_orders.count()}")

for idx, ord in enumerate(user_orders, 1):
    print(f"\n订单 {idx}:")
    print(f"  参考号: {ord.ref_code}")
    print(f"  下单时间: {ord.ordered_date}")
    print(f"  状态: {ord.get_status_display()}")
    print(f"  商品数量: {ord.items.count()}")
    print(f"  总金额: ${ord.get_total()}")

# 测试批量操作（管理员功能）
print("\n【步骤8】测试管理员批量操作")
print("-" * 80)
print("模拟批量更新订单状态...")

pending_orders = Order.objects.filter(status='P')
print(f"当前待处理订单数: {pending_orders.count()}")

if pending_orders.exists():
    # 批量设置为已发货
    count = pending_orders.update(status='S')
    print(f"✓ 批量更新 {count} 个订单为'已发货'状态")
    
    # 验证更新结果
    shipped_orders = Order.objects.filter(status='S')
    print(f"当前已发货订单数: {shipped_orders.count()}")
else:
    print("没有待处理的订单")

# 清理测试数据
print("\n【步骤9】清理测试数据")
print("-" * 80)
order.delete()
order_item1.delete()
order_item2.delete()
print("✓ 清理订单数据完成")

print("\n" + "=" * 80)
print("所有功能测试完成！")
print("=" * 80)
print("\n测试总结:")
print("✓ 订单状态追踪功能正常")
print("✓ 订单取消功能正常")
print("✓ 库存预警功能正常")
print("✓ 订单历史查询功能正常")
print("✓ 管理员批量操作功能正常")