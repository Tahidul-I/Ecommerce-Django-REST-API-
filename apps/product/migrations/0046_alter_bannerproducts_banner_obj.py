# Generated by Django 5.0.3 on 2024-09-12 03:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0012_allbanner'),
        ('product', '0045_productvariation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerproducts',
            name='banner_obj',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='banner', to='banner.allbanner'),
        ),
    ]
