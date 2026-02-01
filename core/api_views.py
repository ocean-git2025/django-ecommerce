from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.db import models
from core.models import ORDER_STATUS_CHOICES
import json

from .models import Item, Order, OrderItem


@require_GET
def check_stock(request, item_id):
    """
    API端点：检查商品库存
    返回JSON格式的库存信息，包括是否低库存
    """
    item = get_object_or_404(Item, id=item_id)
    data = {
        'item_id': item.id,
        'title': item.title,
        'stock': item.stock,
        'stock_threshold': item.stock_threshold,
        'is_low_stock': item.is_low_stock(),
        'is_out_of_stock': item.stock <= 0,
        'price': item.price,
        'discount_price': item.discount_price,
    }
    return JsonResponse(data)


@require_GET
def check_multiple_stocks(request):
    """
    API端点：检查多个商品的库存
    接受逗号分隔的商品ID列表
    """
    item_ids = request.GET.get('ids', '').split(',')
    if not item_ids or item_ids == ['']:
        return JsonResponse({'error': '未提供商品ID'}, status=400)
    
    try:
        item_ids = [int(id) for id in item_ids]
    except ValueError:
        return JsonResponse({'error': '无效的商品ID'}, status=400)
    
    items_data = []
    for item_id in item_ids:
        try:
            item = Item.objects.get(id=item_id)
            items_data.append({
                'item_id': item.id,
                'title': item.title,
                'stock': item.stock,
                'stock_threshold': item.stock_threshold,
                'is_low_stock': item.is_low_stock(),
                'is_out_of_stock': item.stock <= 0,
                'price': item.price,
                'discount_price': item.discount_price,
            })
        except Item.DoesNotExist:
            items_data.append({
                'item_id': item_id,
                'error': '商品不存在'
            })
    
    return JsonResponse({'items': items_data})


@require_GET
def get_low_stock_items(request):
    """
    API端点：获取所有低库存商品
    """
    low_stock_items = Item.objects.filter(stock__lte=models.F('stock_threshold')).order_by('stock')
    items_data = []
    
    for item in low_stock_items:
        items_data.append({
            'item_id': item.id,
            'title': item.title,
            'stock': item.stock,
            'stock_threshold': item.stock_threshold,
            'is_out_of_stock': item.stock <= 0,
            'price': item.price,
            'discount_price': item.discount_price,
            'category': item.get_category_display(),
        })
    
    return JsonResponse({'items': items_data, 'count': len(items_data)})


@login_required
@require_GET
def get_order_status(request, order_ref_code):
    """
    API端点：获取订单状态
    """
    order = get_object_or_404(Order, ref_code=order_ref_code, user=request.user)
    data = {
        'ref_code': order.ref_code,
        'status': order.status,
        'status_display': order.get_status_display(),
        'ordered_date': order.ordered_date,
        'being_delivered': order.being_delivered,
        'received': order.received,
        'can_cancel': order.can_cancel(),
    }
    return JsonResponse(data)


@login_required
@require_GET
def get_user_orders(request):
    """
    API端点：获取用户的所有订单
    """
    orders = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    orders_data = []
    
    for order in orders:
        orders_data.append({
            'ref_code': order.ref_code,
            'status': order.status,
            'status_display': order.get_status_display(),
            'ordered_date': order.ordered_date,
            'total': order.get_total(),
            'can_cancel': order.can_cancel(),
        })
    
    return JsonResponse({'orders': orders_data})


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class UpdateOrderStatusView(View):
    """
    API端点：更新订单状态（仅限管理员或订单所有者取消订单）
    """
    def post(self, request, order_ref_code):
        order = get_object_or_404(Order, ref_code=order_ref_code)
        
        # 检查权限：只有订单所有者可以取消订单，管理员可以更新任何状态
        if not request.user.is_staff and order.user != request.user:
            return JsonResponse({'error': '权限不足'}, status=403)
        
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if not new_status:
                return JsonResponse({'error': '未提供状态'}, status=400)
            
            # 非管理员只能取消订单
            if not request.user.is_staff and new_status != 'X':
                return JsonResponse({'error': '只能取消订单'}, status=400)
            
            # 验证状态是否有效
            valid_statuses = [choice[0] for choice in ORDER_STATUS_CHOICES]
            if new_status not in valid_statuses:
                return JsonResponse({'error': '无效的状态'}, status=400)
            
            # 更新状态
            old_status = order.status
            order.status = new_status
            order.save()
            
            # 如果是取消订单，恢复库存
            if new_status == 'X' and old_status != 'X':
                for order_item in order.items.all():
                    order_item.item.stock += order_item.quantity
                    order_item.item.save()
            
            return JsonResponse({
                'success': True,
                'old_status': old_status,
                'new_status': new_status,
                'status_display': order.get_status_display()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class UpdateStockView(View):
    """
    API端点：更新商品库存（仅限管理员）
    """
    def post(self, request, item_id):
        if not request.user.is_staff:
            return JsonResponse({'error': '权限不足'}, status=403)
        
        item = get_object_or_404(Item, id=item_id)
        
        try:
            data = json.loads(request.body)
            new_stock = data.get('stock')
            new_threshold = data.get('stock_threshold')
            
            if new_stock is not None:
                try:
                    new_stock = int(new_stock)
                    if new_stock < 0:
                        return JsonResponse({'error': '库存不能为负数'}, status=400)
                    item.stock = new_stock
                except ValueError:
                    return JsonResponse({'error': '无效的库存值'}, status=400)
            
            if new_threshold is not None:
                try:
                    new_threshold = int(new_threshold)
                    if new_threshold < 0:
                        return JsonResponse({'error': '阈值不能为负数'}, status=400)
                    item.stock_threshold = new_threshold
                except ValueError:
                    return JsonResponse({'error': '无效的阈值'}, status=400)
            
            item.save()
            
            return JsonResponse({
                'success': True,
                'item_id': item.id,
                'title': item.title,
                'stock': item.stock,
                'stock_threshold': item.stock_threshold,
                'is_low_stock': item.is_low_stock(),
                'is_out_of_stock': item.stock <= 0,
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)