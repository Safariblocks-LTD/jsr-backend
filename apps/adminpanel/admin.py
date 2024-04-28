from django.contrib import admin
from django.utils import timezone
from .actions import (
    pre_approve_maintenance,
    approve_maintenance,
    pre_approve_reward,
    approve_reward,
    reject_maintenance_request,
    reject_reward_request,
    update_contract_data,
    update_console_data,
    SmartContract
    )
from .models import (
    PreApprovalMaintenanceRequestModel,
    ApprovalMaintenanceModel,
    PreRewardRequestModel,
    RewardRequestModel,
    Feedback,
    LocationAddress, 
    RejectedClaimModel,
    RejectedRewardModel,
    ApprovedClaimModel,
    ApprovedRewardModel,
    ContractData,
    ContractFund,
    WithdrawFund,
    ConsoleData,
    TitleUnderMaintenance
    )
from django.contrib.auth.models import User, Group



admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(LocationAddress)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = ["email", "subject", "description", "datetime"] 

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(TitleUnderMaintenance)
class TitleUnderMaintenanceAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_claim_status=0, payment_status=1,maintenance_expire_on__lt= timezone.now())
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PreApprovalMaintenanceRequestModel)
class PreMaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ["title","maintenance_status" , "maintenance_claim_status", "ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]

    actions = [pre_approve_maintenance, reject_maintenance_request]
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_claim_status=3, maintenance_reward_status=0)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(ApprovalMaintenanceModel)
class ApprovalMaintenanceAdmin(admin.ModelAdmin):
    list_display = ["title", "maintenance_status", "maintenance_claim_status","ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]
    actions = [approve_maintenance , reject_maintenance_request]
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_claim_status=4, maintenance_reward_status=0)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(PreRewardRequestModel)
class PreRewardRequestAdmin(admin.ModelAdmin):
    list_display = ["title", "maintenance_status", "maintenance_claim_status", "maintenance_reward_status", "ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_claim_status=0, maintenance_reward_status=1)
    actions = [pre_approve_reward, reject_reward_request]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(RewardRequestModel)
class UnlockRewardAdmin(admin.ModelAdmin):
    list_display = ["title", "maintenance_status", "maintenance_claim_status", "maintenance_reward_status", "ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]
    actions = [approve_reward, reject_reward_request]
    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_claim_status=0, maintenance_reward_status=4)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    


@admin.register(RejectedClaimModel)
class RejectClaimAdmin(admin.ModelAdmin):
    list_display = ["title", "maintenance_status", "maintenance_claim_status", "maintenance_reward_status", "ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_claim_status=1)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RejectedRewardModel)
class RejectedRewardAdmin(admin.ModelAdmin):
    list_display = ["title", "maintenance_status", "maintenance_claim_status", "maintenance_reward_status", "ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_reward_status=3)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



@admin.register(ApprovedClaimModel)
class ApprovedClaimAdmin(admin.ModelAdmin):
    list_display = ["title", "maintenance_status", "maintenance_claim_status", "maintenance_reward_status", "ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_claim_status=2)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ApprovedRewardModel)
class ApprovedRewardAdmin(admin.ModelAdmin):
    list_display = ["title", "maintenance_status", "maintenance_claim_status", "maintenance_reward_status", "ticker_name" ,"premium_in_usd", "maintenance_applied_on","maintenance_expire_on"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(maintenance_reward_status=2)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
   

@admin.register(ContractData)
class ContractDataAdmin(admin.ModelAdmin):
    list_display = ["contract_name", "contract_id", "contract_address", "algo_balance", "usdc_balance", "unlock_balance", "last_update"]

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    fields = ("contract_name", "contract_id", "usdc_unit", "unlock_unit")
    actions = [update_contract_data]
    

@admin.register(ContractFund)
class ContractFundAdmin(admin.ModelAdmin):
    list_display = ["contract", "algo_amount", "txn_id", "datetime"]
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    fields = ('contract','algo_amount') 
    def save_model(self, request, obj, form, change) -> None:
        if not change:
                amount = int(obj.algo_amount)
                obj.txn_id = SmartContract.contract_fund(obj.contract.contract_address, amount)
                obj.algo_amount = round(amount/1000000, 3)
        return super().save_model(request, obj, form, change)
    

@admin.register(WithdrawFund)
class WithdrawFundAdmin(admin.ModelAdmin):
    list_display = ["contract", "usdc_amount", "txn_id", "datetime"]
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    fields = ('contract', 'usdc_amount',) 
    def save_model(self, request, obj, form, change) -> None:
        if not change:
                amount = int(obj.usdc_amount)
                obj.txn_id = SmartContract.withdraw_fund_usdc(obj.contract.contract_name, amount, obj.contract.usdc_unit)
                obj.usdc_amount = round(amount/1000000,3)
        return super().save_model(request, obj, form, change)
    

@admin.register(ConsoleData)
class ConsoleDataAdmin(admin.ModelAdmin):
    list_display = ["app_id", "maintenance_pool_amount", "total_claimed", "titles_in_maintain_total", "titles_maintained_total"]
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        data = queryset.first()
        if not data:
            ConsoleData.objects.SetData()
        return queryset

    actions = [update_console_data]