# Generated by Django 5.0.3 on 2024-08-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbox', '0008_alter_chatroom_update_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectAnonymousChatData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=18, null=True)),
            ],
            options={
                'verbose_name_plural': 'Anonymous User Chat Data',
            },
        ),
    ]
