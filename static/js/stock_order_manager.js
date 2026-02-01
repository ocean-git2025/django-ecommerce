// 库存和订单状态管理的JavaScript工具

// 库存管理工具
const StockManager = {
    // 检查单个商品库存
    async checkStock(itemId) {
        try {
            const response = await fetch(`/api/stock/${itemId}/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error checking stock:', error);
            throw error;
        }
    },

    // 检查多个商品库存
    async checkMultipleStocks(itemIds) {
        try {
            const response = await fetch(`/api/stocks/?ids=${itemIds.join(',')}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error checking multiple stocks:', error);
            throw error;
        }
    },

    // 获取低库存商品
    async getLowStockItems() {
        try {
            const response = await fetch('/api/low-stock-items/');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error getting low stock items:', error);
            throw error;
        }
    },

    // 更新商品库存（管理员功能）
    async updateStock(itemId, stock, stockThreshold) {
        try {
            const data = {};
            if (stock !== undefined) data.stock = stock;
            if (stockThreshold !== undefined) data.stock_threshold = stockThreshold;

            const response = await fetch(`/api/stock/${itemId}/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error updating stock:', error);
            throw error;
        }
    },

    // 更新库存显示
    updateStockDisplay(itemId, stockData) {
        const stockElement = document.getElementById(`stock-${itemId}`);
        if (!stockElement) return;

        stockElement.textContent = stockData.stock;

        // 更新库存状态样式
        if (stockData.is_out_of_stock) {
            stockElement.className = 'badge badge-danger';
        } else if (stockData.is_low_stock) {
            stockElement.className = 'badge badge-warning';
        } else {
            stockElement.className = 'badge badge-success';
        }

        // 更新低库存警告
        const warningElement = document.getElementById(`low-stock-warning-${itemId}`);
        if (warningElement) {
            if (stockData.is_low_stock) {
                warningElement.style.display = 'block';
                warningElement.textContent = `库存警告：仅剩 ${stockData.stock} 件`;
            } else {
                warningElement.style.display = 'none';
            }
        }

        // 更新添加到购物车按钮
        const addToCartBtn = document.getElementById(`add-to-cart-${itemId}`);
        if (addToCartBtn) {
            if (stockData.is_out_of_stock) {
                addToCartBtn.disabled = true;
                addToCartBtn.textContent = '缺货';
                addToCartBtn.className = 'btn btn-secondary disabled';
            } else {
                addToCartBtn.disabled = false;
                addToCartBtn.textContent = '加入购物车';
                addToCartBtn.className = 'btn btn-primary add-to-cart';
            }
        }

        // 更新数量选择器
        const quantitySelect = document.getElementById(`quantity-${itemId}`);
        if (quantitySelect) {
            // 清空现有选项
            quantitySelect.innerHTML = '';
            
            // 添加新选项，最多10个或库存数量
            const maxQuantity = Math.min(10, stockData.stock);
            for (let i = 1; i <= maxQuantity; i++) {
                const option = document.createElement('option');
                option.value = i;
                option.textContent = i;
                quantitySelect.appendChild(option);
            }
        }
    },

    // 初始化库存显示
    initStockDisplay(itemIds) {
        if (itemIds.length === 0) return;

        this.checkMultipleStocks(itemIds)
            .then(data => {
                data.items.forEach(item => {
                    if (!item.error) {
                        this.updateStockDisplay(item.item_id, item);
                    }
                });
            })
            .catch(error => {
                console.error('Error initializing stock display:', error);
            });
    }
};

// 订单状态管理工具
const OrderManager = {
    // 获取订单状态
    async getOrderStatus(orderRefCode) {
        try {
            const response = await fetch(`/api/order/${orderRefCode}/status/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error getting order status:', error);
            throw error;
        }
    },

    // 获取用户所有订单
    async getUserOrders() {
        try {
            const response = await fetch('/api/orders/');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error getting user orders:', error);
            throw error;
        }
    },

    // 更新订单状态
    async updateOrderStatus(orderRefCode, status) {
        try {
            const response = await fetch(`/api/order/${orderRefCode}/status/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ status })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error updating order status:', error);
            throw error;
        }
    },

    // 更新订单状态显示
    updateOrderStatusDisplay(orderRefCode, statusData) {
        // 更新状态徽章
        const statusBadge = document.getElementById(`order-status-${orderRefCode}`);
        if (statusBadge) {
            statusBadge.textContent = statusData.status_display;
            
            // 更新徽章样式
            statusBadge.className = 'badge';
            switch (statusData.status) {
                case 'P':
                    statusBadge.classList.add('badge-warning');
                    break;
                case 'S':
                    statusBadge.classList.add('badge-info');
                    break;
                case 'D':
                    statusBadge.classList.add('badge-primary');
                    break;
                case 'C':
                    statusBadge.classList.add('badge-success');
                    break;
                case 'X':
                    statusBadge.classList.add('badge-danger');
                    break;
            }
        }

        // 更新取消按钮
        const cancelBtn = document.getElementById(`cancel-order-${orderRefCode}`);
        if (cancelBtn) {
            if (statusData.can_cancel) {
                cancelBtn.style.display = 'inline-block';
            } else {
                cancelBtn.style.display = 'none';
            }
        }
    },

    // 初始化订单状态显示
    initOrderStatusDisplay(orderRefCodes) {
        if (orderRefCodes.length === 0) return;

        orderRefCodes.forEach(orderRefCode => {
            this.getOrderStatus(orderRefCode)
                .then(statusData => {
                    this.updateOrderStatusDisplay(orderRefCode, statusData);
                })
                .catch(error => {
                    console.error(`Error initializing order status for ${orderRefCode}:`, error);
                });
        });
    },

    // 设置订单状态自动刷新
    setupAutoRefresh(orderRefCodes, intervalMinutes = 5) {
        if (orderRefCodes.length === 0) return;

        setInterval(() => {
            orderRefCodes.forEach(orderRefCode => {
                this.getOrderStatus(orderRefCode)
                    .then(statusData => {
                        this.updateOrderStatusDisplay(orderRefCode, statusData);
                    })
                    .catch(error => {
                        console.error(`Error refreshing order status for ${orderRefCode}:`, error);
                    });
            });
        }, intervalMinutes * 60 * 1000);
    },

    // 取消订单
    async cancelOrder(orderRefCode) {
        try {
            const response = await fetch(`/api/order/${orderRefCode}/status/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    status: 'X'
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // 更新订单状态显示
                this.getOrderStatus(orderRefCode)
                    .then(statusData => {
                        this.updateOrderStatusDisplay(orderRefCode, statusData);
                    })
                    .catch(error => {
                        console.error(`Error updating order status after cancellation:`, error);
                    });
                
                return { success: true, message: '订单已成功取消' };
            } else {
                return { success: false, message: data.error || '取消订单失败' };
            }
        } catch (error) {
            console.error('Error cancelling order:', error);
            return { success: false, message: '取消订单时发生错误' };
        }
    },

    // 更新订单状态（管理员功能）
    async updateOrderStatus(orderRefCode, newStatus) {
        try {
            const response = await fetch(`/api/order/${orderRefCode}/status/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    status: newStatus
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // 更新订单状态显示
                this.getOrderStatus(orderRefCode)
                    .then(statusData => {
                        this.updateOrderStatusDisplay(orderRefCode, statusData);
                    })
                    .catch(error => {
                        console.error(`Error updating order status after change:`, error);
                    });
                
                return { success: true, message: '订单状态已成功更新' };
            } else {
                return { success: false, message: data.error || '更新订单状态失败' };
            }
        } catch (error) {
            console.error('Error updating order status:', error);
            return { success: false, message: '更新订单状态时发生错误' };
        }
    }
};

// 工具函数：获取CSRF令牌
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 如果是商品列表页，初始化库存显示
    if (document.querySelector('.product-list')) {
        const productElements = document.querySelectorAll('[data-item-id]');
        const itemIds = Array.from(productElements).map(el => el.getAttribute('data-item-id'));
        
        if (itemIds.length > 0) {
            StockManager.initStockDisplay(itemIds);
        }
    }

    // 如果是订单历史页，初始化订单状态显示
    if (document.querySelector('.order-history')) {
        const orderElements = document.querySelectorAll('[data-order-ref]');
        const orderRefCodes = Array.from(orderElements).map(el => el.getAttribute('data-order-ref'));
        
        if (orderRefCodes.length > 0) {
            OrderManager.initOrderStatusDisplay(orderRefCodes);
            // 设置每5分钟自动刷新一次订单状态
            OrderManager.setupAutoRefresh(orderRefCodes, 5);
        }
        
        // 添加订单取消按钮事件监听器
        document.querySelectorAll('[id^="cancel-order-"]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const orderRefCode = this.id.replace('cancel-order-', '');
                
                if (confirm('确定要取消这个订单吗？')) {
                    OrderManager.cancelOrder(orderRefCode)
                        .then(result => {
                            if (result.success) {
                                alert(result.message);
                                // 刷新页面或更新UI
                                window.location.reload();
                            } else {
                                alert('错误: ' + result.message);
                            }
                        })
                        .catch(error => {
                            console.error('Error cancelling order:', error);
                            alert('取消订单时发生错误，请稍后再试');
                        });
                }
            });
        });
    }

    // 如果是管理员页面，初始化低库存警告
    if (document.querySelector('.admin-dashboard')) {
        StockManager.getLowStockItems()
            .then(data => {
                const lowStockCountElement = document.getElementById('low-stock-count');
                if (lowStockCountElement) {
                    lowStockCountElement.textContent = data.count;
                }
                
                const lowStockListElement = document.getElementById('low-stock-list');
                if (lowStockListElement && data.items.length > 0) {
                    lowStockListElement.innerHTML = '';
                    data.items.forEach(item => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item d-flex justify-content-between align-items-center';
                        li.innerHTML = `
                            <div>
                                <strong>${item.title}</strong>
                                <br>
                                <small class="text-muted">库存: ${item.stock} / 阈值: ${item.stock_threshold}</small>
                            </div>
                            <span class="badge badge-danger badge-pill">${item.stock}</span>
                        `;
                        lowStockListElement.appendChild(li);
                    });
                }
            })
            .catch(error => {
                console.error('Error initializing low stock warnings:', error);
            });
    }
});

// 导出工具供其他脚本使用
window.StockManager = StockManager;
window.OrderManager = OrderManager;