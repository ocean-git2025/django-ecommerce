# 前端开发文档

## 1. 页面结构说明

### 1.1 用户界面页面

#### 1.1.1 首页 (home.html)
- **功能**: 展示商品概览、热门商品和促销信息
- **关键元素**:
  - 导航栏
  - 商品轮播图
  - 热门商品展示
  - 库存状态显示
- **JavaScript依赖**: main.js, stock_order_manager.js

#### 1.1.2 商品列表页 (product_list.html)
- **功能**: 展示所有商品，支持筛选和排序
- **关键元素**:
  - 商品网格布局
  - 分类筛选器
  - 价格排序
  - 库存状态显示
  - 低库存警告
- **JavaScript功能**:
  - 动态库存更新
  - 添加到购物车
  - 实时筛选和排序

#### 1.1.3 商品详情页 (product_detail.html)
- **功能**: 展示商品详细信息，支持购买
- **关键元素**:
  - 商品图片
  - 详细描述
  - 价格和库存信息
  - 数量选择器
  - 添加到购物车按钮
- **JavaScript功能**:
  - 实时库存检查
  - 数量验证
  - 购物车更新

#### 1.1.4 购物车页 (order_summary.html)
- **功能**: 管理购物车商品，进行结算
- **关键元素**:
  - 商品列表
  - 数量调整控件
  - 价格计算
  - 结算按钮
- **JavaScript功能**:
  - 数量调整
  - 价格自动计算
  - 库存验证

#### 1.1.5 订单结算页 (checkout.html)
- **功能**: 完成订单结算流程
- **关键元素**:
  - 收货地址表单
  - 支付方式选择
  - 订单确认
  - 库存警告
- **JavaScript功能**:
  - 表单验证
  - 库存检查
  - 订单提交

#### 1.1.6 用户中心页 (profile.html)
- **功能**: 管理个人信息和查看订单
- **关键元素**:
  - 用户信息
  - 订单历史
  - 订单状态显示
  - 库存状态查看
- **JavaScript功能**:
  - 订单状态实时更新
  - 订单取消
  - 库存状态检查

### 1.2 管理员界面页面

#### 1.2.1 管理员仪表板 (admin/dashboard.html)
- **功能**: 展示系统概览和关键指标
- **关键元素**:
  - 订单统计
  - 低库存警告
  - 快速操作按钮
- **JavaScript功能**:
  - 实时数据更新
  - 低库存警告

#### 1.2.2 批量操作页 (admin/bulk_operations.html)
- **功能**: 批量管理订单和库存
- **关键元素**:
  - 订单筛选器
  - 批量选择
  - 批量操作按钮
- **JavaScript功能**:
  - 批量选择
  - 订单状态更新
  - 库存管理

## 2. 前后端对接要点

### 2.1 API接口

#### 2.1.1 库存管理API
- **获取单个商品库存**: `GET /api/stock/{item_id}/`
- **获取多个商品库存**: `GET /api/stocks/?ids={id1,id2,...}`
- **获取低库存商品**: `GET /api/low-stock-items/`
- **更新商品库存**: `POST /api/stock/{item_id}/update/`

#### 2.1.2 订单管理API
- **获取订单状态**: `GET /api/order/{order_ref_code}/status/`
- **更新订单状态**: `POST /api/order/{order_ref_code}/status/update/`
- **取消订单**: `POST /api/order/{order_ref_code}/cancel/`

### 2.2 数据格式

#### 2.2.1 库存数据格式
```json
{
  "id": 1,
  "title": "商品名称",
  "stock": 10,
  "stock_threshold": 5,
  "is_low_stock": true
}
```

#### 2.2.2 订单状态数据格式
```json
{
  "ref_code": "ORDER123",
  "status": "P",
  "status_display": "待处理",
  "ordered_date": "2023-01-01T12:00:00Z"
}
```

### 2.3 错误处理
- 所有API请求应包含适当的错误处理
- 使用try-catch块捕获网络错误
- 显示用户友好的错误消息
- 记录详细的错误信息用于调试

### 2.4 认证和授权
- 所有API请求需要包含CSRF令牌
- 管理员操作需要管理员权限
- 用户操作需要用户登录状态

## 3. JavaScript模块说明

### 3.1 main.js
- **功能**: 提供通用功能和初始化代码
- **主要函数**:
  - `initTooltips()`: 初始化工具提示
  - `initModals()`: 初始化模态框
  - `initFormValidation()`: 初始化表单验证
  - `initStockManager()`: 初始化库存管理器
  - `initOrderManager()`: 初始化订单管理器
  - `getCookie(name)`: 获取Cookie值
  - `showMessage(message, type)`: 显示通知消息
  - `formatPrice(price)`: 格式化价格
  - `formatDate(dateString)`: 格式化日期
  - `debounce(func, wait)`: 防抖函数

### 3.2 stock_order_manager.js
- **功能**: 处理库存和订单状态管理
- **主要对象**:
  - `StockManager`: 库存管理工具
    - `checkStock(itemId)`: 检查单个商品库存
    - `checkMultipleStocks(itemIds)`: 检查多个商品库存
    - `getLowStockItems()`: 获取低库存商品
    - `updateStock(itemId, stock, stockThreshold)`: 更新商品库存
    - `updateStockDisplay(itemId, stockData)`: 更新库存显示
    - `getStock(itemId)`: 获取库存
  - `OrderManager`: 订单管理工具
    - `checkOrderStatus(orderRefCode)`: 检查订单状态
    - `cancelOrder(orderRefCode)`: 取消订单
    - `updateOrderStatus(orderRefCode, newStatus)`: 更新订单状态
    - `updateOrderStatusDisplay(orderRefCode, statusData)`: 更新订单状态显示
    - `getOrderStatus(orderRefCode)`: 获取订单状态

## 4. 使用指南

### 4.1 开发环境设置
1. 确保Django服务器正在运行
2. 确保静态文件已正确配置
3. 确保JavaScript文件已部署到正确位置

### 4.2 添加新功能
1. 在相应的HTML模板中添加必要的HTML结构
2. 在JavaScript文件中添加相应的功能代码
3. 确保所有API调用包含适当的错误处理
4. 测试功能在各种情况下的表现

### 4.3 调试技巧
1. 使用浏览器开发者工具查看网络请求
2. 检查控制台错误信息
3. 使用console.log输出调试信息
4. 使用断点调试JavaScript代码

### 4.4 性能优化
1. 使用防抖函数减少不必要的API调用
2. 合理设置更新间隔
3. 使用缓存减少重复请求
4. 优化图片加载

### 4.5 常见问题解决
1. **静态文件加载失败**: 检查STATIC_URL和STATICFILES_DIRS配置
2. **API请求失败**: 检查URL配置和CSRF令牌
3. **库存显示不更新**: 检查JavaScript初始化和事件监听器
4. **订单状态不更新**: 检查API响应和显示更新逻辑

## 5. 代码规范

### 5.1 JavaScript代码规范
1. 使用const和let而不是var
2. 使用箭头函数而不是function关键字
3. 使用模板字符串而不是字符串拼接
4. 使用适当的注释
5. 遵循一致的命名约定

### 5.2 HTML模板规范
1. 使用语义化HTML标签
2. 添加适当的ARIA属性提高可访问性
3. 使用一致的缩进和格式
4. 添加适当的注释

### 5.3 CSS样式规范
1. 使用BEM命名约定
2. 避免使用!important
3. 使用相对单位而不是固定单位
4. 优化选择器性能

## 6. 测试指南

### 6.1 单元测试
1. 测试JavaScript函数的输入输出
2. 测试API调用的成功和失败情况
3. 测试错误处理逻辑

### 6.2 集成测试
1. 测试前端与后端的交互
2. 测试完整的用户流程
3. 测试各种边界情况

### 6.3 用户界面测试
1. 测试响应式设计
2. 测试可访问性
3. 测试浏览器兼容性

## 7. 部署指南

### 7.1 生产环境配置
1. 压缩JavaScript和CSS文件
2. 设置适当的缓存头
3. 配置CDN加速静态资源
4. 启用Gzip压缩

### 7.2 监控和维护
1. 监控JavaScript错误
2. 监控API性能
3. 定期更新依赖库
4. 定期进行安全审计