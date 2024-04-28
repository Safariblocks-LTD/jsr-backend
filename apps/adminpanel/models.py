from apps.asset.models import AssetMaintenanceStatus
from django.db import models
from django.utils import timezone
from utils.smartcontract import SmartContract
from django.conf import settings
from utils.helpers import Helper

class Feedback(models.Model):
    subject = models.CharField(max_length=300, verbose_name="Name")
    description = models.TextField()
    email = models.EmailField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subject 
    


class LocationAddressManager(models.Manager):
    def get_all_addresses_by_search(self, search):
        if search:
            return self.filter(address__icontains=search)
        return self.all()
    
    
    def get_nearest_locations(self, latitude, longitude, num_locations=5):
        return (
            self.get_queryset()
            .annotate(
                distance=(
                    (models.F('latitude') - latitude) ** 2 +
                    (models.F('longitude') - longitude) ** 2
                ) ** 0.5
            )
            .order_by('distance')[:num_locations]
        )
    

class LocationAddress(models.Model):
    address = models.TextField()
    pincode = models.CharField(max_length=6, default='000000')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    objects = LocationAddressManager()

    def __str__(self) -> str:
        return self.address
    
    class Meta:
        verbose_name_plural = "Pick-up Locations"

class PreApprovalMaintenanceRequestModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = 'Pre-Approval Maintenance Claim Request'
        verbose_name_plural = '1 Pre-Approval Maintenance Claim Requests'


class PreRewardRequestModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = "Pre-Approval Maintenance Reward"
        verbose_name_plural = "1 Pre-Approval Maintenance Reward"  


class ApprovalMaintenanceModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = 'Approval Maintenance Claim'
        verbose_name_plural = '2 Approval Maintenance Claim'


class RewardRequestModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = "Approval Maintenance Reward"
        verbose_name_plural = "2 Approval Maintenance Rewards"


class RejectedRewardModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = "Rejected Reward Maintenance Reward"
        verbose_name_plural = "3 Rejected Reward Maintenance Rewards"


class RejectedClaimModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = "Rejected Claim Maintenance "
        verbose_name_plural = "3 Rejected Claim Maintenance"


class ApprovedClaimModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = "Approved Claim Maintenance "
        verbose_name_plural = "4 Approved Claim Maintenance"


class ApprovedRewardModel(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name = "Approved Reward Maintenance Reward"
        verbose_name_plural = "4 Approved Reward Maintenance Rewards"


class TitleUnderMaintenance(AssetMaintenanceStatus):
    class Meta:
        proxy = True
        verbose_name_plural = "0 Title Under Maintenance"
        

class ContractData(models.Model):
    contract_name = models.CharField(max_length=50,default="")
    contract_id = models.IntegerField(default=0)
    contract_address = models.CharField(max_length=200)
    algo_balance = models.FloatField(default=0)
    usdc_balance = models.FloatField(default=0)
    unlock_balance = models.FloatField(default=0)
    usdc_unit = models.IntegerField(default=0)
    unlock_unit = models.IntegerField(default=0)
    algo_balance_func = models.CharField(max_length=50, default="")
    usdc_balance_func = models.CharField(max_length=50, default="")
    unlock_balance_func = models.CharField(max_length=50, default="")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.contract_name} {self.contract_id}"

    class Meta:
        db_table = "contract_data"
        verbose_name_plural = "Contract Balance"


class ContractFund(models.Model):
    contract = models.ForeignKey(ContractData,null=True, on_delete=models.SET_NULL)
    algo_amount = models.FloatField()
    txn_id = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.txn_id} {self.algo_amount}"


class WithdrawFund(models.Model):
    contract = models.ForeignKey(ContractData, null=True, on_delete=models.SET_NULL)
    usdc_amount = models.FloatField()
    txn_id = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.usdc_amount} {self.txn_id}"
    


class ConsoleDataManager(models.Manager):
    def SetData(self, app_id=settings.CONSOLE_SMART_APP_ID):
        obj= self.filter(app_id=app_id).first()
        if not obj:
            data = SmartContract.console_data()
            new_obj = self.create(
            app_id = settings.CONSOLE_SMART_APP_ID,
            maintenance_pool_total =Helper.round_asset_count_to_decimal(data.get("maintenance_pool_total")),
            total_claimed = data.get("total_claimed"),
            titles_in_maintain_total = data.get("titles_in_maintain_total"),
            titles_maintained_total = data.get("titles_maintained_total"))
            return new_obj
        data = SmartContract.console_data()
        obj.maintenance_pool_total = data.get("maintenance_pool_total")
        obj.total_claimed = data.get("total_claimed")
        obj.titles_in_maintain_total = data.get("titles_in_maintain_total")
        obj.titles_maintained_total = data.get("titles_maintained_total")
        obj.save()
        return obj

    
class ConsoleData(models.Model):
    app_id = models.IntegerField()
    maintenance_pool_total = models.FloatField()
    total_claimed = models.IntegerField()
    titles_in_maintain_total = models.IntegerField()
    titles_maintained_total = models.IntegerField()
    objects = ConsoleDataManager()

    def maintenance_pool_amount(self):
        return f"{self.maintenance_pool_total} $"
    
    class Meta:
        verbose_name_plural = "Console Records"