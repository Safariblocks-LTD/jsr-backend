# Generated by Django 3.2.15 on 2022-09-08 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_device_request_mobile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='request_mobile',
            new_name='requested_mobile',
        ),
    ]
