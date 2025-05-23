# Generated by Django 5.0.3 on 2024-06-20 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('banner_url', models.CharField(max_length=1500)),
            ],
        ),
        migrations.CreateModel(
            name='TitleBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('banner_url', models.CharField(max_length=1500)),
            ],
        ),
    ]
