# Django E-commerce 收藏功能使用说明

## 项目概述

这是一个基于 Django 的电商项目，已经实现了商品展示、分类、购物车、结账和用户登录等基本功能。现在新增了商品收藏功能。

## 新增功能说明

### 1. 商品收藏功能

- **商品详情页**：为已登录的用户显示一个“收藏”按钮。对于未登录的用户，点击按钮时会跳转到登录页面。
- **我的收藏页面**：用户可以在个人中心查看自己收藏的所有商品列表。

### 2. 数据模型

新增了 `ProductFavorite` 模型来记录用户和商品的收藏关系：
- 一个用户可以收藏多个商品
- 一个商品也可以被多个用户收藏

## 运行项目

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 创建超级用户

```bash
python manage.py createsuperuser
```

### 4. 运行开发服务器

```bash
python manage.py runserver
```

### 5. 访问项目

在浏览器中访问 `http://localhost:8000`

## 功能测试

### 1. 收藏商品

1. 访问商品详情页（例如：`http://localhost:8000/product/shirt/`）
2. 登录用户会看到“收藏”按钮
3. 点击按钮后，商品会被添加到收藏夹

### 2. 查看收藏的商品

1. 登录后，点击导航栏中的“我的收藏”链接
2. 可以看到所有收藏的商品列表
3. 可以取消收藏或添加到购物车

### 3. 取消收藏

1. 在商品详情页，如果商品已被收藏，会显示“取消收藏”按钮
2. 点击按钮后，商品会从收藏夹中移除

## 技术实现

### 1. 数据模型

```python
class ProductFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.title}"

    class Meta:
        unique_together = ('user', 'item')
```

### 2. 视图函数

- `add_to_favorites`：添加商品到收藏夹
- `remove_from_favorites`：从收藏夹中移除商品
- `favorites_list`：显示用户收藏的商品列表

### 3. 模板文件

- `product.html`：商品详情页中的收藏按钮
- `favorites.html`：我的收藏页面
- `navbar.html`：导航栏中的“我的收藏”链接

## 注意事项

1. 确保已正确配置数据库连接
2. 收藏功能只对已登录用户开放
3. 一个用户只能收藏同一个商品一次
4. 收藏的商品会显示在“我的收藏”页面中