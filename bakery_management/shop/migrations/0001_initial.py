# Generated by Django 5.0.7 on 2024-11-06 13:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
                ('availability', models.BooleanField(default=True)),
                ('flavor', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
            ],
            options={
                'permissions': [('can_add_product', 'Can add product'), ('can_edit_product', 'Can edit product'), ('can_delete_product', 'Can delete product'), ('can_view_products', 'Can view products')],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('pending', 'Chờ xử lý'), ('delivered', 'Đã giao hàng'), ('completed', 'Hoàn thành'), ('canceled', 'Đã hủy')], default='pending', max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'permissions': [('can_view_orders', 'Can view orders'), ('can_create_order', 'Can create order')],
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discount_type', models.CharField(choices=[('percentage', 'Giảm theo phần trăm'), ('fixed_amount', 'Giảm theo số tiền cố định')], max_length=20)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('products', models.ManyToManyField(related_name='promotions', to='shop.product')),
            ],
            options={
                'verbose_name': 'Khuyến mãi',
                'verbose_name_plural': 'Khuyến mãi',
            },
        ),
    ]
