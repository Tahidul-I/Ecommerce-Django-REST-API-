# Generated by Django 5.0.3 on 2024-07-29 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_orde_abandoned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orde_abandoned',
            field=models.BooleanField(default=True, verbose_name='Cart Abandonment'),
        ),
        migrations.CreateModel(
            name='AbandonCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='abandon_order', to='order.order')),
            ],
        ),
    ]
