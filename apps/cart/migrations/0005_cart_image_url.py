# Generated by Django 5.0.3 on 2024-07-08 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_rename_price_cart_new_price_cart_old_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='image_url',
            field=models.CharField(default=1, max_length=1500),
            preserve_default=False,
        ),
    ]
