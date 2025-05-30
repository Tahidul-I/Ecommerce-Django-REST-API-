# Generated by Django 5.0.3 on 2024-07-15 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_query_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
    ]
