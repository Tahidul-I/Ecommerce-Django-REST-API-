# Generated by Django 5.0.3 on 2024-07-08 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_cart_dimension_cart_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
