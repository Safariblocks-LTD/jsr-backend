# Generated by Django 4.2.7 on 2023-11-22 16:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0013_alter_assetmaintenancestatus_maintenance_expire_on'),
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_id', models.IntegerField(default=0)),
                ('contract_address', models.CharField(max_length=200)),
                ('algo_balanace', models.FloatField()),
                ('usdc_balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ContractFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algo_amount', models.FloatField()),
                ('txn_id', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usdc_amount', models.FloatField()),
                ('txn_id', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovedClaimModel',
            fields=[
            ],
            options={
                'verbose_name': 'Approved Claim Maintenance ',
                'verbose_name_plural': 'Approved Claim Maintenance',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('asset.assetmaintenancestatus',),
        ),
        migrations.CreateModel(
            name='ApprovedRewardModel',
            fields=[
            ],
            options={
                'verbose_name': 'Approved Reward Maintenance Reward',
                'verbose_name_plural': 'Approved Reward Maintenance Rewards',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('asset.assetmaintenancestatus',),
        ),
        migrations.CreateModel(
            name='RejectedClaimModel',
            fields=[
            ],
            options={
                'verbose_name': 'Rejected Claim Maintenance ',
                'verbose_name_plural': 'Rejected Claim Maintenance',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('asset.assetmaintenancestatus',),
        ),
        migrations.CreateModel(
            name='RejectedRewardModel',
            fields=[
            ],
            options={
                'verbose_name': 'Rejected Reward Maintenance Reward',
                'verbose_name_plural': 'Rejected Reward Maintenance Rewards',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('asset.assetmaintenancestatus',),
        ),
    ]
