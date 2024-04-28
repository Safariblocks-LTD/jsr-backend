from rest_framework import serializers
from .models import Brand, TopTokenizedAsset, ChartDataSet
from utils.constants import Constant
from apps.account.models import Account
from utils.aws import Dynamodb
from apps.asset.models import AssetMaintenanceStatus
from apps.transaction.models import ProtocolTransaction
import datetime
from django.db.models import Subquery, OuterRef, TextField, Sum


class TopTokenizedAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopTokenizedAsset
        fields = '__all__'



class BrandSerializer(serializers.ModelSerializer):
    assets = TopTokenizedAssetsSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = '__all__'


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartDataSet
        fields = ["date","price", "get_ticker_name"]


class ProtocolAnalyticSerializer(serializers.Serializer):
    def to_representation(self, instance):
        net_type = self.context["net_type"].upper()
        end = datetime.datetime.now().date()
        end = datetime.datetime.combine(end, datetime.time.min)
        start = end - datetime.timedelta(4)
        instance["value_of_stock"] = Dynamodb.get_value_stock_by_date(start, end, net_type)

        temp_start = start
        locked_property = []
        while temp_start <= end:
            locked_property.append(
                {
                    "value": AssetMaintenanceStatus.objects.filter(
                            maintenance_started_on__lte=temp_start, maintenance_expire_on__gt=temp_start
                        ).annotate(
                            is_valid=Subquery(
                                ProtocolTransaction.objects.filter(title_id=OuterRef('title_id'), activity="Approve Maintenance Claim", date__lte=temp_start).values('title_id'),
                                output_field=TextField()
                            )
                        ).filter(is_valid=None).count(),
                    "date": int(temp_start.timestamp())
                })
            temp_start += datetime.timedelta(1)
        instance["locked_property"] = locked_property

        temp_start = start
        total_locked_value = []
        total_value = AssetMaintenanceStatus.objects.filter(maintenance_started_on__lt=start).aggregate(Sum("premium_in_usd")).get("premium_in_usd__sum", 0)
        if not total_value:
            total_value = 0
        while temp_start <= end:
            usd_rate = AssetMaintenanceStatus.objects.filter(
                            maintenance_started_on=temp_start
                        ).aggregate(Sum("premium_in_usd")).get("premium_in_usd__sum", 0)
            if not usd_rate:
                usd_rate = 0
            total_value += usd_rate
            total_locked_value.append({
                "value": round(total_value, 4),
                "date": int(temp_start.timestamp())
            })
            temp_start += datetime.timedelta(1)
        instance["total_value_locked"] = total_locked_value

        instance["capital_account_created"] = len(set(list(Account.objects.filter(is_imported=True, is_deleted=False).values_list('address'))))
        instance["unique_titles_owned"] = Dynamodb.get_total_bought_title(net_type)
        instance["collateralization_ratio"] = Constant.ANALYTICS_TOTAL_CAPITAL_UNLOCK_RATIO
        return instance
