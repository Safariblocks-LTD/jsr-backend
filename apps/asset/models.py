from django.db import models
from utils import Constant
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Count

class TrendingTokenizableProducts(models.Model):
    image = models.URLField(max_length=255)
    product_title = models.CharField(max_length=300)
    price = models.FloatField()
    affiliate_link = models.URLField(max_length=100)

    def __str__(self) -> str:
        return self.product_title
    

    class Meta:
        db_table = "trending_tokenizable_products"

class AssetVerificationModelManager(models.Manager):

    def getByUuId(self, uuid):
        return self.filter(device_uuid = uuid).first()
    
    def getByTitleId(self, title_id):
        return self.filter(title_id = title_id).first()
    
    def setEmail(self, title_id, email):
        asset_verification = self.getByTitleId(title_id)
        asset_verification.user_email=email
        asset_verification.save()
        return asset_verification
    
    def getById(self, id):
        return self.filter(id = id).first()

    def getUnverifiedByUuId(self, uuid):
        return self.filter(device_uuid = uuid, verification_status = 0).first()
    
    def filterVerifiedByTitleId(self, title_id):
        return self.filter(verification_status=1, title_id__contains=title_id)[0:10]
    
    def filterVerifiedDeviceByTitleId(self, title_id):
        return self.filter(title_id__contains=title_id).exclude(device_brand=None).first()
    
    def filterVerifiedByAssetCategory(self, asset_category):
        asset_category = Constant.deviceCategories.get(asset_category.lower())
        return self.filter(verification_status=1, asset_category=asset_category)[0:10]
    
    def getVerifiedTitles(self, limit, offset):
        return self.filter(verification_status=1).order_by('-id')[offset : offset + limit]
    
    def checkUuid(self, uuid):
        return self.filter(device_uuid = uuid).first()
    
    def getTopTokenizedAssets(self):
        return self.filter(
    title_id__in=AssetMaintenanceStatus.objects.filter(payment_status=1).values('title_id')
).values('device_brand', 'asset_category').annotate(title_count=Count('title_id', distinct=True)).order_by('-title_count')[:12]
    
class AssetVerificationStatus(models.Model):
    user_email = models.EmailField(null=False)
    title_id = models.CharField(max_length=200, null=False, unique=True)
    verified_by = models.CharField(max_length=100, null=False)
    asset_category = models.IntegerField(choices=Constant.choices["AssetCategory"], default=0)
    verification_status = models.IntegerField(choices=Constant.choices["VerificationStatus"], default=0)
    ticker_name = models.CharField(max_length=50, null=True)
    device_name = models.CharField(max_length=50, null=True)
    device_brand = models.CharField(max_length=50, null=True)
    device_uuid = models.CharField(max_length=50)
    index_token = models.IntegerField(null=True)
    ipfs_url = models.CharField(max_length=255, null=True)


    objects = AssetVerificationModelManager()

    class Meta:
        db_table = "asset_verification_status"

class TickerNameModelManager(models.Manager):

    def get_ticker_name(self, brand, category):
        ticker_name = self.filter(brand__iexact = brand, category = category).first().ticker_name
        return ticker_name
    
    def checkBrandExists(self, brand):
        return self.filter(brand__iexact = brand).first()
    
class TickerNameData(models.Model):
    brand = models.CharField(max_length=100)
    category = models.IntegerField(choices=Constant.choices["AssetCategory"])
    ticker_name = models.CharField(max_length=100, unique=True)

    objects = TickerNameModelManager()

    class Meta:
        db_table = "ticker_name_data"

class AssetMaintenanceManager(models.Manager):
        
    def getById(self, id):
        return self.filter(id=id).first()
    
    def getLastByTitleId(self, title_id):
        return self.filter(title_id=title_id).order_by('-id').first()
    
    def getSecuredAssets(self, title_id, limit, offset):
        if title_id:
            assets = self.filter(payment_status=1, title_id__title_id__contains=title_id, maintenance_reward_status=0).distinct().order_by('-id')[0:10]
        else:
            assets = self.filter(payment_status=1, maintenance_reward_status=0).distinct().order_by('-id')[offset : offset + limit]
        return assets
    
    def getLastMaintainedByTitleId(self, title_id):
        return self.filter(title_id=title_id, payment_status=1).order_by('-id').first()
    
    def getProcessedTitleForReward(self, title_id):
        return self.filter(payment_status=1, maintenance_reward_status__gte=1, title_id=title_id).order_by('-id').first()

    def getAllMaintainedByTitleId(self, title_id):
        return self.filter(title_id=title_id, payment_status=1).order_by('-id')
    
class AssetMaintenanceStatus(models.Model):
    title_id = models.ForeignKey(AssetVerificationStatus, on_delete=models.CASCADE, related_name="maintenance_status", to_field="title_id", db_column="title_id")
    maintenance_period = models.IntegerField()
    currency_selected = models.CharField(max_length=20)
    premium_in_usd = models.FloatField()
    premium_in_selected_currency = models.FloatField()
    maintenance_applied_on = models.DateField(auto_now_add=True)
    maintenance_started_on = models.DateField(default=timezone.now)
    maintenance_expire_on = models.DateField(default=timezone.now)
    payment_status = models.IntegerField(choices=Constant.choices["PaymentStatus"], default = 0)
    damage_type = models.IntegerField(choices=Constant.choices["DamageType"], default=0)
    maintenance_claim_status = models.IntegerField(choices=Constant.choices["ClaimStatus"], default=0)
    maintenance_reward_status = models.IntegerField(choices=Constant.choices["MaintenanceRewardStatus"], default=0)
    objects = AssetMaintenanceManager()

    @property
    def title(self):
        return f"#{self.title_id.title_id}"
    
    def __str__(self) -> str:
        return f"{self.title_id.title_id}"

    @property
    def ticker_name(self):
        return self.title_id.ticker_name


    @property
    def maintenance_status(self):
        if not self.payment_status:
            return "Unmaintained"
        elif self.maintenance_expire_on < timezone.now().date():
            return "Maintenance Expired"
        else:
            return "Under Maintenance"

    class Meta:
        db_table = "asset_maintenance_status"


class DevicePriceData(models.Model):
    brand = models.CharField(max_length=255)
    device_category = models.IntegerField(choices=Constant.choices["AssetCategory"])
    price = models.FloatField()
    price_year = models.IntegerField()

    class Meta:
        db_table = "device_price_data"

