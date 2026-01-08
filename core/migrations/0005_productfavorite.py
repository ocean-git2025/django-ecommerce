from django.db import migrations, models
import django.conf


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(django.conf.settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20190630_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=models.deletion.CASCADE, to='core.Item')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to=django.conf.settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'item')},
            },
        ),
    ]