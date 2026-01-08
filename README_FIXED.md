# Django E-commerce 收藏功能修复说明

## 问题修复

### 1. 数据库迁移问题
- 已创建 `0005_productfavorite.py` 迁移文件
- 修复了 ProductFavorite 模型的数据库表生成问题

### 2. 个人资料页集成
- 创建了 `templates/account/profile.html` 模板文件
- 将收藏列表集成到个人资料页中
- 添加了简单的标签页切换功能

### 3. Django Admin 注册
- 在 `core/admin.py` 中注册了 ProductFavorite 模型
- 现在可以在后台管理收藏数据

### 4. 模板标签
- 在 `core/templatetags/cart_template_tags.py` 中添加了 `is_favorited` 模板标签
- 用于判断商品是否已被收藏

## 运行和测试

### 1. 运行项目

```bash
# 创建并应用数据库迁移
python manage.py makemigrations
python manage.py migrate

# 运行开发服务器
python manage.py runserver
```

### 2. 测试功能

1. **收藏商品**：
   - 访问商品详情页（例如：`http://localhost:8000/product/shirt/`）
   - 登录用户会看到“收藏”按钮
   - 点击按钮后，商品会被添加到收藏夹

2. **查看收藏的商品**：
   - 登录后，点击导航栏中的“个人资料”链接
   - 切换到“我的收藏”标签页
   - 可以看到所有收藏的商品列表
   - 可以取消收藏或添加到购物车

3. **取消收藏**：
   - 在商品详情页，如果商品已被收藏，会显示“取消收藏”按钮
   - 点击按钮后，商品会从收藏夹中移除

### 3. 后台管理

- 访问 `http://localhost:8000/admin`
- 登录后可以在“Product favorites”中管理收藏数据

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
- `favorites_list`：显示收藏列表
- `profile`：个人资料页，包含收藏列表

### 3. URL 配置

```python
path('profile/', profile, name='profile'),
path('favorites/', favorites_list, name='favorites'),
path('add-to-favorites/<slug>/', add_to_favorites, name='add-to-favorites'),
path('remove-from-favorites/<slug>/', remove_from_favorites, name='remove-from-favorites')
```

### 4. 模板标签

```python
@register.filter
def is_favorited(user, item):
    if user.is_authenticated:
        return ProductFavorite.objects.filter(user=user, item=item).exists()
    return False
```

## 注意事项

1. 确保已正确配置数据库连接
2. 收藏功能只对已登录用户开放
3. 一个用户只能收藏同一个商品一次
4. 收藏的商品会显示在个人资料页的“我的收藏”标签页中