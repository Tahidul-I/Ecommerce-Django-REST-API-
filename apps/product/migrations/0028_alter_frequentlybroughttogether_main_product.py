# Generated by Django 5.0.3 on 2024-07-06 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_alter_frequentlybroughttogether_main_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequentlybroughttogether',
            name='main_product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='frequently_brought_together', to='product.product'),
        ),
    ]
