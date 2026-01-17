# Generated migration for category choices update

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190630_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('C', '服装'), ('A', '配饰'), ('D', '数码')], max_length=2),
        ),
    ]
