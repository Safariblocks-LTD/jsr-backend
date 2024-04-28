from django.contrib import admin
from django.db import transaction
from algosdk.logic import get_application_address
from django.utils import timezone
from utils.smartcontract import SmartContract
from apps.adminpanel.models import ContractData, ConsoleData
from utils.helpers import Helper
from apps.transaction.models import ProtocolTransaction
from django.conf import settings


@admin.action(description="Pre-Approve Maintenance")
def pre_approve_maintenance(modeladmin, request, queryset):
    for query in queryset:
        query.maintenance_claim_status = 4
        query.save()


@admin.action(description="Approve Maintenance")
def approve_maintenance(modeladmin, request, queryset):
    for query in queryset:
        with transaction.atomic():
            txn_id = SmartContract.console_approve_maintenance_claim(query.title_id.title_id)
            if txn_id:
                ProtocolTransaction.objects.create(
                    tx_id = txn_id,
                    title_id=query.title_id.title_id,
                    activity= "Approve Maintenance Claim",
                    account = settings.ADMIN_ADDRESS,
                )
                query.maintenance_claim_status = 2
                query.save()

@admin.action(description="Pre-Approval Maintenance Reward")
def pre_approve_reward(modeladmin, request, queryset):
    for query in queryset:
        query.maintenance_reward_status = 4
        query.save()


@admin.action(description="Approval Maintenance Reward")
def approve_reward(modeladmin, request, queryset):
    for query in queryset:
        with transaction.atomic():
            txn_id = SmartContract.console_approve_unlock_reward(query.title_id.title_id)
            if txn_id:
                ProtocolTransaction.objects.create(
                    tx_id = txn_id,
                    title_id=query.title_id.title_id,
                    activity= "Approve Maintenance Reward",
                    account = settings.ADMIN_ADDRESS,
                )
                query.maintenance_reward_status = 2
                query.save()


@admin.action(description="Reject Maintenance Request")
def reject_maintenance_request(modeladmin, request, queryset):
    for query in queryset:
        query.maintenance_claim_status = 1
        query.save()


@admin.action(description="Reject Maintenance Reward Request")
def reject_reward_request(modeladmin, request, queryset):
    for query in queryset:
        query.maintenance_reward_status = 3
        query.save()
        

@admin.action(description="Update Data")
def update_contract_data(modeladmin, request, queryset):
    for query in queryset:
        query.contract_address = get_application_address(query.contract_id)
        query.algo_balance = Helper.round_asset_count_to_decimal(SmartContract.get_app_algo_balance(query.contract_name, query.contract_address))
        query.usdc_balance = Helper.round_asset_count_to_decimal(SmartContract.get_app_usdc_balance(query.contract_name, query.usdc_unit))
        query.unlock_balance = Helper.round_asset_count_to_decimal(SmartContract.get_app_unlock_balance(query.contract_name,query.unlock_unit))
        query.last_update = timezone.now
        query.save()



@admin.action(description="Update Data")
def update_console_data(modeladmin, request, queryset):
    for query in queryset:
        ConsoleData.objects.SetData(query.app_id)