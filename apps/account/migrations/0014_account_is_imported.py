# Generated by Django 4.1 on 2024-02-12 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_device_fcm_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_imported',
            field=models.BooleanField(default=False),
        ),
    ]
