from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190630_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='item',
            name='stock_threshold',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('PENDING', '待处理'),
                    ('SHIPPED', '已发货'),
                    ('DELIVERING', '配送中'),
                    ('COMPLETED', '已完成'),
                    ('CANCELLED', '已取消'),
                ],
                default='PENDING',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
