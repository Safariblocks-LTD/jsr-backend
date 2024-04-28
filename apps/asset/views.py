from rest_framework.views import APIView
from utils import (
    Responder, 
    Algorand,
    Dynamodb,
    Helper,
    Constant
)
from utils.validators import Validator
from .serializers import (
    AllAssetListSerializer, 
    OptInAssetOrCloseOutAssetSerializer,
    TrendingTokenizableProductSerializer,
    AssetVerificationSerializer,
    SecuredAssetSerializer,
    TopTokenizedAssetSerializer,
    AssetMaintenanceSerializer,
    MyAssetDetailSerializer,
    GetAccountAssetsSerializer,
    GetAlgorandAssetsSerializer
)
from apps.transaction.serializers import TransactionListSerializer
from jasiri_wallet.permissions import Public
from .models import TrendingTokenizableProducts as TrendingProducts, AssetVerificationStatus, TickerNameData, AssetMaintenanceStatus
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from utils.email import Email
from apps.analytics.models import TopTokenizedAsset
from apps.account.models import Account


class GetAssetOrOptInAssetOrCloseOutAsset(APIView):
    
    def get(self, request, **kwargs):
        queryparams = Validator.get_all_assets_queryparams(request)
        assets =  Algorand.get_all_assets(**queryparams)
        assets = AllAssetListSerializer(assets).data
        return Responder.send(108 if len(assets.get("assets")) else 109, assets)
    
    def post(self, request, **kwargs):  
        serializer = OptInAssetOrCloseOutAssetSerializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(101)
    
    
class GetMyAssetTransaction(APIView):
    
    def get(self, request, **kwargs):
        query = {"asset-id":kwargs["id"], "address":request.user.address}
        transactions =  Algorand.get_txns_history(**query)
        transactions = TransactionListSerializer(transactions, context={"user":request.user}).data
        return Responder.send(106 if len(transactions) else 110, transactions)
    

class BoughtUnboughtTitles(APIView):
    permission_classes = (Public,)
    def get(self, request, **kwargs):
        bought = request.GET.get('bought')
        title_id = request.GET.get('title_id')
        data_limit = int(request.GET.get('limit',100))
        chain = kwargs['net_type'].upper()
        exclusive_start_key = eval(request.GET.get('LastEvaluatedKey')) if request.GET.get('LastEvaluatedKey') else None
        Responder.raise_error(506) if bought is None and not title_id else None
        bought = not bought == 'true'
        titles = Dynamodb.bought_unbought_titles(bought, chain, title_id, data_limit, exclusive_start_key)
        return Responder.send(140, titles)
    
    
class TrendingTokenizableProducts(APIView):
    permission_classes = [Public]

    def get(self, request, **kwargs):
        queryset = TrendingProducts.objects.all()
        serializer = TrendingTokenizableProductSerializer(queryset, many=True)
        return Responder.send(141, serializer.data)
    
    

class SendMailToVerifyTitle(APIView):
    permission_classes = (Public,)
    def post(self, request, **kwargs):
        data = request.data
        email = data.get('user_email')
        title_id = data.get('title_id')
        chain = kwargs.get('net_type')
        is_title, ipfs_url, is_owner, _ = Dynamodb.getTitle(title_id, chain.upper())
        if not is_title or not is_owner:
            return Responder.raise_error(157)
        if asset := AssetVerificationStatus.objects.getByTitleId(title_id):
            uuid = asset.device_uuid
            title_id = asset.title_id
            if not asset.index_token:
                AssetVerificationStatus.objects.setEmail(title_id, email)
                url = f'/v1/{chain}/assets/update-title-status/'+str(uuid)
                Email.send_verify_asset_mail(url, title_id, email)
                return Responder.send(146, {'url':url})
            return Responder.raise_error(174)
        data['ipfs_url'] = ipfs_url
        serializer = AssetVerificationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        uuid = serializer.data.get('device_uuid') 
        url = f'/v1/{chain}/assets/update-title-status/'+str(uuid)
        Email.send_verify_asset_mail(url, title_id, email)
        return Responder.send(146, {'url':url})
    

class VerifyTitle(APIView):
    permission_classes = []
    def get(self, request, uuid, **kwargs):
        if not AssetVerificationStatus.objects.checkUuid(uuid):
            return Responder.send(147)
        device_details = Helper.get_device_details(request.META.get('HTTP_USER_AGENT', ''))
        if not TickerNameData.objects.checkBrandExists(device_details.get('device').get('brand')):
            return Responder.send(142, status=False)
        asset_obj = AssetVerificationStatus.objects.getUnverifiedByUuId(uuid)
        if not asset_obj:
            return Responder.send(143, status=False)
        # if device_details.get('device').get('type').lower() == asset_obj.get_asset_category_display().lower():
        ticker_name = Helper.get_ticker_name(device_details.get('device').get('brand'), device_details.get('device').get('type'))
        data = {
            "ticker_name": ticker_name,
            "device_name": device_details.get('device').get('name'),
            "verification_status": 0,
            "device_brand":device_details.get('device').get('brand'),
        }
        TopTokenizedAsset.objects.increase_vol(ticker_name)
        serializer = AssetVerificationSerializer(asset_obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(144)


class GetVerifiedTitles(APIView):
    permission_classes = (Public,)
    def get(self, request, **kwargs):
        if request.GET.get('title_id'):
            assets = AssetVerificationStatus.objects.filterVerifiedByTitleId(request.GET.get('title_id'))
        elif request.GET.get('asset_category'):
            assets = AssetVerificationStatus.objects.filterVerifiedByAssetCategory(request.GET.get('asset_category'))
        else:  
            limit  = int(request.GET.get('limit', 10))
            offset = (int(request.GET.get('page_no', 1)) - 1) * limit  
            assets = AssetVerificationStatus.objects.getVerifiedTitles(limit, offset)
        serializer = AssetVerificationSerializer(assets, many=True)
        return Responder.send(148, serializer.data)


class GetTitleDetails(APIView):
    permission_classes = (Public,)
    def get(self, request, **kwargs):
        titles = AssetVerificationStatus.objects.filterVerifiedByTitleId(request.GET.get('title_id'))
        if not titles:
            return Responder.raise_error(157)
        serializer = AssetVerificationSerializer(titles[0])
        return Responder.send(149, serializer.data)


class GetTitleDevice(APIView):
    permission_classes = (Public,)
    def get(self, request, **kwargs):
        title = AssetVerificationStatus.objects.filterVerifiedDeviceByTitleId(request.GET.get('title_id'))
        if not title:
            return Responder.raise_error(157)
        serializer = AssetVerificationSerializer(title)
        return Responder.send(149, serializer.data)
    

class GetMaintenancePremium(APIView):
    permission_classes = (Public,)

    def post(self, request, **kwargs):
        data = request.data
        chain = kwargs.get('net_type')
        title_id = data.get("title_id")
        _, _, _, price = Dynamodb.getTitle(title_id,chain.upper())
        if not price:
            return Responder.raise_error(173)
        premium_in_usd = (int(price) / int(36*1000000)) * int(data.get('maintenance_period'))
        premium_in_currency = Helper.convert_premium_to_selected_currency(premium_in_usd, data.get('currency_selected'))
        data["premium_in_usd"] = round(premium_in_usd, 6)
        data["premium_in_selected_currency"] = round(premium_in_currency,6)
        last_obj = AssetMaintenanceStatus.objects.getLastByTitleId(data.get('title_id'))
        if not last_obj:
            serializer = AssetMaintenanceSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        elif last_obj.maintenance_status == "Maintenance Expired":
            serializer = AssetMaintenanceSerializer(last_obj, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        elif last_obj.maintenance_status == "Under Maintenance":
            return Responder.send(153)
        updated_obj = AssetMaintenanceStatus.objects.getLastByTitleId(data.get('title_id'))
        serializer = SecuredAssetSerializer(updated_obj)
        return Responder.send(150, serializer.data)
    
    
    def put(self, request, **kwargs):
        data = request.data
        id = data.get('id')
        obj = AssetMaintenanceStatus.objects.getById(id)
        if not obj:
            return Responder.send(151)
        if data["success"]:
            data["payment_status"] = 1
            data["maintenance_started_on"] = timezone.now().date()
            data["maintenance_expire_on"] = timezone.now().date() + relativedelta(months=obj.maintenance_period)
        serializer = AssetMaintenanceSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Responder.send(152, serializer.data)

class GetSecuredAssets(APIView):
    permission_classes = (Public,)
    def get(self, request, **kwargs):
        limit = int(request.GET.get('limit', 10))
        offset = (int(request.GET.get('page_no', 1)) - 1) * limit
        title_id = request.GET.get('title_id')
        assets = AssetMaintenanceStatus.objects.getSecuredAssets(title_id, limit, offset)
        serializer = SecuredAssetSerializer(assets, many=True)     
        return Responder.send(155, serializer.data) 
    
    
class UpdateIndexToken(APIView):
    permission_classes = (Public,)
    def put(self, request, **kwargs):
        obj = AssetVerificationStatus.objects.getByTitleId(request.data.get('title_id'))
        serializer = AssetVerificationSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(154, serializer.data)


class VerifyTitleId(APIView):
    permission_classes = (Public,)
    def get(self, request, **kwargs):
        title_id = request.GET.get('title_id')
        chain = kwargs.get('net_type').upper()
        is_title = Dynamodb.getTitle(title_id, chain)
        return Responder.send(156) if is_title else Responder.send(157)
   
    
class FileMaintenanceClaim(APIView):
    permission_classes = [Public]

    def post(self, request, **kwargs):
        data = request.data
        if not Dynamodb.getTitle(data.get('title_id'), kwargs.get('net_type').upper())[0]:
            return Responder.send(157)
        title_obj = AssetMaintenanceStatus.objects.getLastMaintainedByTitleId(data.get('title_id'))
        if not title_obj:
            return Responder.send(159)
        if title_obj.maintenance_status != 'Under Maintenance':
            resp_data = {'maintenance_status':title_obj.maintenance_status}
            return Responder.send(158, resp_data)
        data["maintenance_claim_status"] = 3 if not data.get('update_claim_status') else data.get('update_claim_status')
        serializer = AssetMaintenanceSerializer(title_obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(160) if not data.get('update_claim_status') else Responder.send(161)
        

class ClaimMaintenanceReward(APIView):
    permission_classes = [Public]
    def post(self, request, **kwargs):
        data = request.data
        title_id = data.get('title_id')
        if not Dynamodb.getTitle(data.get('title_id'), kwargs.get('net_type').upper())[0]:
            return Responder.send(157)
        obj = AssetMaintenanceStatus.objects.getLastMaintainedByTitleId(title_id)
        if obj.maintenance_status != 'Maintenance Expired' or obj.maintenance_claim_status in [2, 3] or obj.maintenance_reward_status in [1, 2]:
            return Responder.send(162)
        obj.maintenance_reward_status = 1
        obj.save()
        return Responder.send(163)
    
    
class UpdateRewardStatus(APIView):
    def post(self, request, **kwargs):
        data = request.data
        obj = AssetMaintenanceStatus.objects.getProcessedTitleForReward(data.get('title_id'))
        serializer = AssetMaintenanceSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(164)
    

class TopTokenizedAssets(APIView):
    permission_classes = [Public]
    def get(self, request, **kwargs):
        result = AssetVerificationStatus.objects.getTopTokenizedAssets()
        serializer = TopTokenizedAssetSerializer(result, many=True)
        return Responder.send(165, serializer.data)
    

class TitleMaintenancePrice(APIView):
    permission_classes = (Public,)
    def get(self, request, **kwargs):
        chain = kwargs.get('net_type')
        title_id = request.GET.get('title_id')
        maintenance_period = request.GET.get('maintenance_period')
        _, _, _, price = Dynamodb.getTitle(title_id,chain.upper())
        if not price:
            return Responder.raise_error(173)
        premium_in_usd = (int(price) / int(36*1000000)) * int(maintenance_period)
        premium_in_usd = round(premium_in_usd, 6)
        data = {
            "title_id": title_id,
            "maintenance_period": maintenance_period,
            "premium_in_usd": premium_in_usd
        }    
        return Responder.send(178, data)


class ConvertUSDCTo(APIView):
    permission_classes = (Public,)

    def get(self, request, **kwargs):
        premium_in_usd = request.GET.get('premium_in_usd')
        currency_selected = request.GET.get('currency_selected')

        premium_in_currency = Helper.convert_premium_to_selected_currency(premium_in_usd, currency_selected)

        data = {
            "premium_in_usd": premium_in_usd,
            "premium_in_currency": premium_in_currency,
            "currency_selected": currency_selected
            }
        return Responder.send(179, data)


class GetAccountAssets(APIView):
    permission_classes = (Public,)

    def get(self, request, address, **kwargs):
        Validator.validate_address(address=address)
        secondary_currency = request.GET.get('secondary_currency')
        queryset = Account.objects.get_by_device_and_address(request.user.id, address)
        details = []
        if queryset and queryset.is_imported:
            details = Algorand.get_account_info(queryset.address)
            details = GetAccountAssetsSerializer(details["assets"], many=True, context={"secondary_currency": secondary_currency, "net_type": kwargs.get("net_type")}).data
        return Responder.send(108, details)


class GetAlgorandAsset(APIView):
    permission_classes = (Public,)

    def get(self, request, **kwargs):
        asset_type = request.query_params.get("asset-type")
        queryparams = Validator.get_all_assets_queryparams(request)
        assets = Algorand.get_all_assets(**queryparams)
        assets = GetAlgorandAssetsSerializer(assets, context={"asset_type": asset_type}).data
        next_page_token = assets.pop("next-token")
        assets["next_page_token"] = next_page_token
        return Responder.send(108 if len(assets.get("assets")) else 109, assets)


class DashboardView(APIView):
    permission_classes = (Public,)

    def get(self, request, **kwargs):
        secondary_currency = request.GET.get('secondary_currency', 'USD')
        queryset = Account.objects.filter(device_id=request.user.id, is_deleted=False, is_imported=True)
        total_amount = 0
        total_algo = 0
        for account in queryset:
            details = Algorand.get_account_info(account.address)
            details = GetAccountAssetsSerializer(details["assets"], many=True, context={"secondary_currency": secondary_currency, "net_type": kwargs.get("net_type")}).data
            for detail in details:
                amount = 0
                if detail.get("id") == 0:
                    total_algo += detail.get("amount").get("secondary", {}).get("value", 0)
                    continue
                if (
                    detail.get("id") in getattr(Constant, f"{kwargs.get('net_type').upper()}_VERIFIED_ASSET_ID_LIST")
                    and detail.get("amount").get("secondary", {}).get("value", 0)
                    and detail.get("id") not in [0, 180447, 312769]
                ):
                    amount = detail.get("amount").get("secondary", {}).get("value", 0)
                total_amount = total_amount + amount
        algo_change_percentage = Helper.get_portfolio_percentage(total_algo, total_amount, secondary_currency)
        return Responder.send(
            138, {
                    "total_amount": round(total_amount + total_algo, 2),
                    "secondary_currency": secondary_currency,
                    "total_tiles": 0,
                    "algo_change_percentage": round(algo_change_percentage, 2),
                    "title_change_percentage": 0
                }
        )


class GetAssetGraphView(APIView):
    permission_classes = (Public,)

    def get(self, request, **kwargs):
        params = request.query_params
        days = int(params.get("days")) if params.get("days") else 5
        if not params.get("asset_name") or not params.get("secondary_currency"):
            return Responder.raise_error(506)
        asset_name = Constant.COINGEKO_COIN_ID.get(params.get("asset_name").lower(), params.get("asset_name"))
        data = {}
        graphs = Helper.get_asset_graph_data(asset_name, params.get("secondary_currency"))
        data["market_cap"] = graphs.get("market_caps", [])[-days:] if graphs.get("market_caps", []) else []
        data["exchange_price"] = graphs.get("prices", [])[-days:] if graphs.get("prices", []) else []
        data["today_percentage_change"] = Helper.percent_24h_change_currency(asset_name, params.get("secondary_currency"))
        return Responder.send(203, data)


class TitleDetailsDynamoDB(APIView):
    permission_classes = (Public,)

    def get(self, request, **kwargs):
        params = request.query_params
        title = Dynamodb.get_title_details(params.get("extCID"), kwargs["net_type"].upper())
        return Responder.send(156 if title else 157, title)
