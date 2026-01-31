from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

ORDER_STATUS_PENDING = 'PENDING'
ORDER_STATUS_SHIPPED = 'SHIPPED'
ORDER_STATUS_DELIVERING = 'DELIVERING'
ORDER_STATUS_COMPLETED = 'COMPLETED'
ORDER_STATUS_CANCELLED = 'CANCELLED'

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS_PENDING, '待处理'),
    (ORDER_STATUS_SHIPPED, '已发货'),
    (ORDER_STATUS_DELIVERING, '配送中'),
    (ORDER_STATUS_COMPLETED, '已完成'),
    (ORDER_STATUS_CANCELLED, '已取消'),
)

ORDER_STATUS_MAPPING = dict(ORDER_STATUS_CHOICES)

STATUS_TRANSITIONS = {
    ORDER_STATUS_PENDING: [ORDER_STATUS_SHIPPED, ORDER_STATUS_CANCELLED],
    ORDER_STATUS_SHIPPED: [ORDER_STATUS_DELIVERING],
    ORDER_STATUS_DELIVERING: [ORDER_STATUS_COMPLETED],
    ORDER_STATUS_COMPLETED: [],
    ORDER_STATUS_CANCELLED: [],
}


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    """商品模型"""
    title = models.CharField(max_length=100, verbose_name='商品名称')
    price = models.FloatField(verbose_name='价格')
    discount_price = models.FloatField(blank=True, null=True, verbose_name='折扣价')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, verbose_name='分类')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, verbose_name='标签')
    slug = models.SlugField(verbose_name='URL标识')
    description = models.TextField(verbose_name='商品描述')
    image = models.ImageField(upload_to='products/', verbose_name='商品图片')
    stock = models.IntegerField(default=0, verbose_name='库存数量')
    stock_threshold = models.IntegerField(default=10, verbose_name='库存预警阈值')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.title

    def clean(self):
        if self.stock < 0:
            raise ValidationError({'stock': '库存数量不能为负数'})
        if self.stock_threshold < 0:
            raise ValidationError({'stock_threshold': '库存预警阈值不能为负数'})

    def is_low_stock(self):
        """判断库存是否低于预警阈值"""
        return self.stock <= self.stock_threshold

    def update_stock(self, quantity):
        """更新库存数量，quantity为正数表示增加，负数表示减少"""
        new_stock = self.stock + quantity
        if new_stock < 0:
            raise ValidationError('库存不足，无法完成扣减')
        self.stock = new_stock
        self.save()

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    """订单模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    ref_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='订单号')
    items = models.ManyToManyField(OrderItem, verbose_name='订单商品')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    ordered_date = models.DateTimeField(verbose_name='下单时间')
    ordered = models.BooleanField(default=False, verbose_name='已下单')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES,
                              default=ORDER_STATUS_PENDING, verbose_name='订单状态')
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name='收货地址')
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL,
        blank=True, null=True, verbose_name='账单地址')
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='支付记录')
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='优惠券')
    being_delivered = models.BooleanField(default=False, verbose_name='配送中')
    received = models.BooleanField(default=False, verbose_name='已收货')
    refund_requested = models.BooleanField(default=False, verbose_name='申请退款')
    refund_granted = models.BooleanField(default=False, verbose_name='同意退款')
    shipped_date = models.DateTimeField(blank=True, null=True, verbose_name='发货时间')
    delivering_date = models.DateTimeField(blank=True, null=True, verbose_name='配送开始时间')
    completed_date = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-ordered_date']

    def __str__(self):
        return f"{self.ref_code} - {self.user.username}"

    def get_total(self):
        """计算订单总金额"""
        total = sum(order_item.get_final_price() for order_item in self.items.all())
        if self.coupon:
            total -= self.coupon.amount
        return max(total, 0)

    def can_cancel(self):
        """判断订单是否可以取消（只有待处理状态可取消）"""
        return self.status == ORDER_STATUS_PENDING

    def get_status_display_cn(self):
        """获取订单状态的中文显示"""
        return ORDER_STATUS_MAPPING.get(self.status, '未知')

    def can_transition_to(self, new_status):
        """判断是否可以转换到指定状态"""
        allowed_transitions = STATUS_TRANSITIONS.get(self.status, [])
        return new_status in allowed_transitions

    def update_status(self, new_status):
        """更新订单状态，带状态转换验证"""
        if new_status == self.status:
            return True
        if not self.can_transition_to(new_status):
            raise ValidationError(
                f'无法从「{self.get_status_display_cn()}」转换到「{ORDER_STATUS_MAPPING.get(new_status, "未知")}」'
            )
        self.status = new_status
        self.save()
        return True

    def cancel(self):
        """取消订单"""
        if not self.can_cancel():
            raise ValidationError('该订单无法取消')
        self.status = ORDER_STATUS_CANCELLED
        self.save()
        return True


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
