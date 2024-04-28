# Generated by Django 4.1 on 2023-10-22 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0005_assetmaintenancestatus_maintenance_expire_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetmaintenancestatus',
            name='damage_type',
            field=models.IntegerField(choices=[(0, 'No Damage'), (1, 'Water Damage'), (2, 'Screen Damage'), (3, 'Physical Damage')], default=0),
        ),
        migrations.AddField(
            model_name='assetmaintenancestatus',
            name='maintenance_claim_status',
            field=models.IntegerField(choices=[(0, 'Not Claimed'), (1, 'Rejected'), (2, 'Approved'), (3, 'In Progress')], default=0),
        ),
    ]
