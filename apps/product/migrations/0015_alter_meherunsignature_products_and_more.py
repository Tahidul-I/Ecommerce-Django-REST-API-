# Generated by Django 5.0.3 on 2024-06-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_product_is_deal_remove_product_is_signature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meherunsignature',
            name='products',
            field=models.ManyToManyField(related_name='signature', to='product.productvariation'),
        ),
        migrations.AlterField(
            model_name='ourbestdeals',
            name='products',
            field=models.ManyToManyField(related_name='top_deals', to='product.productvariation'),
        ),
    ]
