from django.db import models
from django.utils import timezone
from utils.helpers import Helper


class Brand(models.Model):
    name = models.CharField(max_length=200)
    img_url = models.URLField()

    def __str__(self) -> str:
        return self.name
    

class TopTokenizedAssetManager(models.Manager):
    def increase_vol(self, ticker_name):
        tokenized_asset = self.filter(ticker_name=ticker_name).first()
        if tokenized_asset:
            tokenized_asset.vol +=1
            tokenized_asset.save()
        cache_key = 'TOP_TOKENIZED_ASSETS'
        Helper.deleteCacheData(cache_key)
        return tokenized_asset


class TopTokenizedAsset(models.Model):
    ticker_name = models.CharField(max_length=10)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="assets")
    market_price = models.IntegerField(default=0, null=False)
    vol = models.IntegerField(default=0)
    objects = TopTokenizedAssetManager()

    class Meta:
        db_table = "top_tokenized_assets"

    def __str__(self) -> str:
        return f"{self.ticker_name} {self.brand}"
    


class ChartDataSetManager(models.Manager):

    def get_chart_data_by_ticker(self, ticker_name):
        asset = TopTokenizedAsset.objects.filter(ticker_name=ticker_name).first()
        return self.filter(asset=asset).all()


class ChartDataSet(models.Model):
    asset = models.ForeignKey(TopTokenizedAsset, on_delete=models.CASCADE)
    date = models.DateField(null=False, default=timezone.now)
    price = models.IntegerField(null=False, default=0)
    objects = ChartDataSetManager()


    @property
    def get_ticker_name(self):
        return self.asset.ticker_name

    class Meta:
        db_table = "chart_dataset"