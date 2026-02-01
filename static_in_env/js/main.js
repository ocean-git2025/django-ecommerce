/**
 * Main JavaScript file for the Django E-commerce Application
 * Contains common functions and initialization code
 */

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    initTooltips();
    
    // 初始化模态框
    initModals();
    
    // 初始化表单验证
    initFormValidation();
    
    // 初始化库存管理器
    initStockManager();
    
    // 初始化订单管理器
    initOrderManager();
});

/**
 * 初始化Bootstrap工具提示
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * 初始化Bootstrap模态框
 */
function initModals() {
    const modalTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'));
    modalTriggerList.map(function (modalTriggerEl) {
        return new bootstrap.Modal(modalTriggerEl);
    });
}

/**
 * 初始化表单验证
 */
function initFormValidation() {
    // 获取所有需要验证的表单
    const forms = document.querySelectorAll('.needs-validation');
    
    // 循环遍历表单并添加提交事件监听器
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * 初始化库存管理器
 */
function initStockManager() {
    // 如果页面上有库存相关元素，则初始化库存管理器
    if (document.querySelector('.stock-display') || document.querySelector('.stock-warning')) {
        // 创建库存管理器实例
        window.stockManager = new StockManager();
        
        // 初始化库存显示
        window.stockManager.initStockDisplay();
        
        // 初始化库存警告
        window.stockManager.initStockWarnings();
    }
}

/**
 * 初始化订单管理器
 */
function initOrderManager() {
    // 如果页面上有订单相关元素，则初始化订单管理器
    if (document.querySelector('.order-status') || document.querySelector('.cancel-order-btn')) {
        // 创建订单管理器实例
        window.orderManager = new OrderManager();
        
        // 初始化订单状态显示
        window.orderManager.initOrderStatusDisplay();
        
        // 初始化取消订单按钮
        window.orderManager.initCancelOrderButtons();
    }
}

/**
 * 显示加载指示器
 * @param {string} containerId - 容器ID
 */
function showLoadingIndicator(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="d-flex justify-content-center align-items-center" style="height: 200px;">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">加载中...</span>
                </div>
            </div>
        `;
    }
}

/**
 * 显示错误消息
 * @param {string} containerId - 容器ID
 * @param {string} message - 错误消息
 */
function showErrorMessage(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                ${message}
            </div>
        `;
    }
}

/**
 * 显示成功消息
 * @param {string} containerId - 容器ID
 * @param {string} message - 成功消息
 */
function showSuccessMessage(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-success" role="alert">
                <i class="bi bi-check-circle-fill me-2"></i>
                ${message}
            </div>
        `;
    }
}

/**
 * 格式化价格
 * @param {number} price - 价格
 * @param {string} currency - 货币符号
 * @returns {string} 格式化后的价格
 */
function formatPrice(price, currency = '¥') {
    return currency + parseFloat(price).toFixed(2);
}

/**
 * 格式化日期
 * @param {Date|string} date - 日期
 * @returns {string} 格式化后的日期
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * 获取CSRF令牌
 * @returns {string} CSRF令牌
 */
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

/**
 * 显示通知消息
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型 (success, error, warning, info)
 * @param {number} duration - 显示时长（毫秒）
 */
function showNotification(message, type = 'info', duration = 5000) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 设置自动移除
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, duration);
}

/**
 * 确认对话框
 * @param {string} message - 确认消息
 * @param {Function} callback - 确认后的回调函数
 */
function confirmDialog(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * 刷新页面内容
 * @param {string} url - 请求URL
 * @param {string} containerId - 容器ID
 * @param {Function} callback - 成功后的回调函数
 */
function refreshContent(url, containerId, callback) {
    showLoadingIndicator(containerId);
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            document.getElementById(containerId).innerHTML = html;
            if (callback) {
                callback();
            }
        })
        .catch(error => {
            console.error('Error refreshing content:', error);
            showErrorMessage(containerId, '加载内容失败，请稍后再试。');
        });
}

/**
 * 处理AJAX表单提交
 * @param {HTMLFormElement} form - 表单元素
 * @param {Function} successCallback - 成功后的回调函数
 * @param {Function} errorCallback - 失败后的回调函数
 */
function handleAjaxFormSubmit(form, successCallback, errorCallback) {
    const formData = new FormData(form);
    const url = form.getAttribute('action') || window.location.href;
    const method = form.getAttribute('method') || 'POST';
    
    fetch(url, {
        method: method,
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            if (successCallback) {
                successCallback(data);
            }
        } else {
            if (errorCallback) {
                errorCallback(data.error || '操作失败');
            }
        }
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        if (errorCallback) {
            errorCallback('提交表单时发生错误');
        }
    });
}

/**
 * 初始化图片懒加载
 */
function initLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // 回退方案：直接加载所有图片
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

/**
 * 初始化返回顶部按钮
 */
function initBackToTop() {
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed';
    backToTopButton.style.bottom = '20px';
    backToTopButton.style.right = '20px';
    backToTopButton.style.zIndex = '1000';
    backToTopButton.style.display = 'none';
    backToTopButton.setAttribute('aria-label', '返回顶部');
    
    document.body.appendChild(backToTopButton);
    
    // 滚动事件监听
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    // 点击事件
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 页面加载完成后初始化懒加载和返回顶部按钮
window.addEventListener('load', () => {
    initLazyLoading();
    initBackToTop();
});