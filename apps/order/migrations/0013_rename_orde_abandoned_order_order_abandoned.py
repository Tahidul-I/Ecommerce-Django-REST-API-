# Generated by Django 5.0.3 on 2024-07-30 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_abandoncart_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orde_abandoned',
            new_name='order_abandoned',
        ),
    ]
