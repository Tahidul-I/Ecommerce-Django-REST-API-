# Generated by Django 5.0.3 on 2024-09-04 11:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0041_productvariation_last_selling_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='last_selling_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 4, 11, 29, 25, 561680, tzinfo=datetime.timezone.utc)),
        ),
    ]
