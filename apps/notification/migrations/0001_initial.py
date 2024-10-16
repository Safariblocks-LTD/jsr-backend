# Generated by Django 4.1 on 2022-10-28 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0008_alter_device_country_code_alter_device_mobile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('net', models.CharField(choices=[(1, 'MAIN NET'), (2, 'BETA NET'), (3, 'TEST NET')], max_length=15)),
                ('is_seen', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_notifications', to='account.device')),
            ],
            options={
                'db_table': 'notifications',
            },
        ),
    ]
