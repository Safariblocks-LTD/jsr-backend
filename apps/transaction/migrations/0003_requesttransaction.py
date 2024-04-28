# Generated by Django 4.1 on 2024-02-25 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_account_is_primary'),
        ('transaction', '0002_alter_protocoltransaction_account_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_address', models.CharField(max_length=150)),
                ('to_address', models.CharField(max_length=150)),
                ('asset_id', models.IntegerField()),
                ('asset_name', models.CharField(max_length=255)),
                ('transaction_type', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('is_rejected', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_request_resolved', models.BooleanField(default=False)),
                ('device', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='request_transaction_device', to='account.device')),
            ],
            options={
                'db_table': 'request_transactions',
            },
        ),
    ]
