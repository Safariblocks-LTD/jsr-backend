from rest_framework import serializers
from utils import (
    Responder, 
    Algorand,
    Constant,
    Helper, 
    AlgoExplorer
)
from .models import TrendingTokenizableProducts, AssetVerificationStatus, AssetMaintenanceStatus
from django.core.cache import cache


class AssetDetailSerializer(serializers.Serializer):
    
    def to_representation(self, instance):
        fee = Helper.amount_in_algo(Constant.MIN_TXN_FEE)
        name = instance.get("params").get("name", "Unnamed")
        return {
            "id": instance["index"],
            "name": name,
            "unit": instance.get("params").get("unit-name", "UNNAMED"),
            "short_name": Helper.get_short_name(name),
            "fee": fee,
            "verification": instance.get("verification", {}).get("reputation")
        }
        
        
class MyAssetDetailSerializer(serializers.Serializer):
    
    def to_representation(self, instance):
        asset = AlgoExplorer.asset_id_to_unit_name(instance["asset-id"])
        name = asset.get("asset_name")
        unit = asset.get("unit_name")
        return {
            "id": instance["asset-id"],
            "amount": Helper.microamount_in_algo_usd(
                instance["amount"],
                unit,
                instance["asset-id"],
                self.context.get("secondary_currency", 'USD')
            ),
            "name": name,
            "unit": unit,
            "short_name": Helper.get_short_name(name),
            "verified": bool(instance.get("verification"))
        }
        
        
class AssetListSerializer(serializers.Serializer):
    
    def to_representation(self, instance):
        instance.pop("current-round", None)
        if instance.get("next-token"):
            instance["next_page_token"] = instance.pop("next-token", None)
        return instance        


class AllAssetListSerializer(AssetListSerializer):
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["assets"] = AssetDetailSerializer(instance["assets"], many=True).data
        return response
    
    
class OptInAssetOrCloseOutAssetSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    txn_type = serializers.ChoiceField(choices=Constant.ASSET_OPTIN_CLOSEOUT_CHOICES)
    
    def validate(self, attrs):
        account = Algorand.get_account_info(self.context["user"].address)
        asset = Helper.get_asset_from_assets_by_index(account["assets"], attrs["index"])
        if attrs["txn_type"] == "optin_axfer":
            if asset:
                Responder.raise_error(129)
        else:
            if not asset:
                Responder.raise_error(130)
            if asset.get("amount"):
                Responder.raise_error(131)
            attrs["receiver"] = asset["creator"]
        return attrs
    
    def create(self, attrs):
        attrs["sender"] = self.context["user"].address
        Algorand.transactions(self.context["user"].private_key, **attrs)
        return {}
    

class TrendingTokenizableProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrendingTokenizableProducts
        fields = '__all__'


class AssetVerificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssetVerificationStatus
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data['maintenance_status'] = AssetMaintenanceStatus.objects.filter(title_id=instance.title_id). order_by('-id').first().maintenance_status
        except:
             data['maintenance_status'] = None
        return data
    

class AssetMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMaintenanceStatus
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ipfs_url'] = instance.title_id.ipfs_url
        return data


class SecuredAssetSerializer(serializers.Serializer):

    def to_representation(self, instance):
        # return super().to_representation(instance)
        response = {}
        response['id'] = instance.id
        response["title_id"] = instance.title_id.title_id
        response["maintenance_status"] = instance.maintenance_status
        response["maintenance_period"] = instance.maintenance_period if instance.maintenance_status == "Under Maintenance" else None
        response["ticker_name"] = instance.title_id.ticker_name
        response['ipfs_url'] = instance.title_id.ipfs_url
        response["premium_in_usd"] = instance.premium_in_usd
        response["premium_in_selected_currency"] = instance.premium_in_selected_currency
        response['index_token'] = instance.title_id.index_token
        response['maintenance_claim_status'] = instance.maintenance_claim_status
        response['maintenance_reward_status'] = instance.maintenance_reward_status
        return response


class TopTokenizedAssetSerializer(serializers.Serializer):
    device_brand = serializers.CharField()
    asset_category = serializers.IntegerField()
    title_count = serializers.IntegerField()


class GetAccountAssetsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        if not (asset := cache.get(f"asset_details_{instance.get('asset-id', 0)}_{self.context.get('net_type')}", None)):
            asset = AlgoExplorer.asset_detail_from_asset_id(instance["asset-id"])
            cache.set(
                f"asset_details_{instance.get('asset-id', 0)}_{self.context.get('net_type')}",
                asset,
                7*24*60*60
            )  # set cache for a week
        net_type = self.context.get("net_type").upper()
        unit = asset.get("unit-name", "UNNAMED")
        name = asset.get("name", "Unnamed")
        asset_info = {
                "id": instance["asset-id"],
                "amount": Helper.microamount_in_algo_usd(
                    instance["amount"],
                    unit,
                    instance["asset-id"],
                    self.context.get("secondary_currency", 'USD')
                ),
                "name": name,
                "unit": unit,
                "short_name": Helper.get_short_name(name),
                "verified": True if instance["asset-id"] in getattr(Constant, f"{net_type}_VERIFIED_ASSET_ID_LIST") else False,
            }

        if asset.get("total") == 1:
            asset_info["asset_type"] = "nft"
            asset_info["url"] = asset.get("url")
            return asset_info

        asset_info["asset_type"] = "asset"
        return asset_info


class GetAlgorandAssetsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        assets = []
        for asset in instance["assets"]:
            fee = Helper.amount_in_algo(Constant.MIN_TXN_FEE)
            name = asset.get("params").get("name", "Unnamed")
            temp_asset = {
                "id": asset["index"],
                "name": name,
                "unit": asset.get("params").get("unit-name", "UNNAMED"),
                "short_name": Helper.get_short_name(name),
                "fee": fee,
                "verification": asset.get("verification", {}).get("reputation")
            }

            if self.context["asset_type"] == "nft" and asset.get("params").get("total") == 1:
                temp_asset["asset_type"] = "nft"
                temp_asset["url"] = asset.get("params").get("url")
                assets.append(temp_asset)

            if self.context["asset_type"] == "asset" and asset.get("params").get("total") != 1:
                temp_asset["asset_type"] = "asset"
                assets.append(temp_asset)

        instance["assets"] = assets
        return instance
