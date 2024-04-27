import boto3
from django.conf import settings
from django.core.cache import cache
from utils import Constant
import json
from apps.asset.models import AssetVerificationStatus, AssetMaintenanceStatus
from datetime import timedelta

class Dynamodb():
    dynamodb_client = boto3.client(
        "dynamodb",
        aws_access_key_id = settings.AWS_DYNAMODB_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_DYNAMODB_SECRET_ACCESS_KEY,
        region_name = settings.AWS_DYNAMODB_REGION
    )
    
    @classmethod
    def get_analytics(cls, chain):
        try:
            chain = chain.upper()
            analytics = cache.get(f"{chain}_ANALYTICS")
            if not analytics:
                analytics = cls._analytics(chain)
                cache.set(f"{chain}_ANALYTICS", analytics, Constant.ANALYTICS_EXPIRE_TIME)
            return analytics
        except Exception:
            return cls._on_error_analytics()
        
    @classmethod
    def _analytics(cls, chain):
        response = cls.dynamodb_client.scan(
            TableName = getattr(settings, f"AWS_DYNAMODB_{chain}_TABLE_NAME"),
            ProjectionExpression=Constant.ANALYTICS_BASE_VALUE_INDEX_NAME
        )
        response["Sum"] = cls._total_tokenized_base_value(response["Items"])
        return {
            "Number of Tokenized asset": response["Count"],
            "Total capital unlocked": response["Sum"] * Constant.ANALYTICS_TOTAL_CAPITAL_UNLOCK_RATIO,
            "Total value locked": None,
            "Total asset base value": response["Sum"],
        }
    
    @classmethod
    def _total_tokenized_base_value(cls, assets):
        return sum(float(asset[Constant.ANALYTICS_BASE_VALUE_INDEX_NAME]['N']) for asset in assets)
    
    @classmethod
    def _on_error_analytics(cls):
        return {
            "Number of Tokenized asset": None,
            "Total assets base value": None,
            "Total value locked": None,
            "Total capital unlocked": None,
        }
    

    @classmethod
    def test_main_filter(cls, chain, token_data, limit=100):
        keyword = "test" if chain == "TESTNET" else "main"
        result = []
        for token in token_data:
            if keyword in token.get("asset_id"):
                result.append(token)
            if len(result) >= limit:
                return result
        return result


    @classmethod
    def bought_unbought_titles(cls, bought:bool, chain, title_id=None, limit=100, exclusive_start_key=None):
        client = cls.dynamodb_client
        filter_expression = cls.__getFilterExpression(bought, title_id)
        if exclusive_start_key:
            filter_expression['ExclusiveStartKey'] = exclusive_start_key
        response = client.scan(
            TableName = getattr(settings, f"AWS_DYNAMODB_{chain}_TABLE_NAME"),
            **filter_expression
        )
        tokens = response['Items']
        if bought:
            token_data = [cls.__getUnboughtTokenJson(token) for token in tokens]
        else:
            token_data = [cls.__getBoughtTokenJson(token) for token in tokens]
        if response.get('LastEvaluatedKey'):
            token_data.append({'LastEvaluatedKey':response.get('LastEvaluatedKey')})
        result_data = cls.test_main_filter(chain, token_data, limit)
        return result_data
    
        
    @staticmethod
    def __getFilterExpression(bought, title_id):
        filter_expression = {
            "FilterExpression": "#12e70 = :12e70 And #12e71 = :12e71",
            "ExpressionAttributeNames": {"#12e70":"jsrSent","#12e71":"onSale"},
            "ExpressionAttributeValues": {":12e70": {"BOOL": True},":12e71": {"BOOL": bought}}
        }
        if title_id:
            filter_expression['FilterExpression'] += " And #b7972 = :b7972"
            filter_expression['ExpressionAttributeNames']["#b7972"] = "extCID"
            filter_expression['ExpressionAttributeValues'][":b7972"] = {"N" : str(title_id)}
        return filter_expression
    
    @classmethod
    def __getUnboughtTokenJson(cls, token):
        return {
            'id': cls.__getTokenId(token),
            'title': cls.__getTokenTitle(token),
            'price': cls.__getTokenPrice(token),
            'url': cls.__getTokenURL(token), 
            'asset_id': cls.__getAssetID(token)
        }
    
    @classmethod
    def __getBoughtTokenJson(cls, token):
        token_data = cls.__getUnboughtTokenJson(token)
        token_data["owner"] = cls.__getTokenOwner(token)
        verification_maintenance_data = cls.__getVerificationMaintenanceStatus(token)
        token_data['verification_status'] = verification_maintenance_data[0]
        token_data["maintenance_status"] = verification_maintenance_data[1]
        token_data['ticker_name'] = verification_maintenance_data[2]
        token_data['maintenance_sessions'] = cls.__getMaintenanceSessions(token)
        return token_data
    
    @staticmethod
    def __getTokenTitle(token):
        return token.get('extCID').get('N')
    
    @staticmethod
    def __getTokenPrice(token):
        return token.get('assetValue').get('N')
    
    @staticmethod 
    def __getTokenURL(token):
        commitment = (token.get('commitment').get('S'))
        return json.loads(commitment).get('url')
    
    @staticmethod
    def __getTokenOwner(token):
        return token.get('accountAddr').get('S')
    
    @staticmethod
    def __getTokenId(token):
        return token.get('id').get('S')
    
    @staticmethod
    def __getAssetID(token):
        return token.get('assetID').get('S')
    
    @staticmethod
    def __getVerificationMaintenanceStatus(token):
        title_id = token.get('extCID').get('N')
        if obj := AssetMaintenanceStatus.objects.getLastByTitleId(title_id):
            return (obj.title_id.verification_status, obj.maintenance_status, obj.title_id.ticker_name)
        obj = AssetVerificationStatus.objects.getByTitleId(title_id)
        return (obj.verification_status, None, obj.ipfs_url) if obj else (None, None, None)
    
    @staticmethod
    def __getMaintenanceSessions(token):
        title_id = token.get('extCID').get('N')
        all_objs = AssetMaintenanceStatus.objects.getAllMaintainedByTitleId(title_id)
        return len(all_objs) if all_objs else 0
        
    
    
    @classmethod
    def getTitle(cls, title_id, chain):
        client = cls.dynamodb_client
        filter_expression = {
            "FilterExpression": "#4ff40 = :4ff40",
            "ExpressionAttributeNames": {"#4ff40":"extCID"},
            "ExpressionAttributeValues": {":4ff40": {"N":f"{title_id}"}}
        }
        response = client.scan(
            TableName = getattr(settings, f"AWS_DYNAMODB_{chain}_TABLE_NAME"),
            **filter_expression
        )
        if response.get('Count'):
            token = response['Items']
            img_url = cls.__getTokenURL(token[0])
            owner = cls.__getTokenOwner(token[0])
            price = cls.__getTokenPrice(token[0])
            return (True, img_url, owner, price)
        return (False, None, None, None)

    @classmethod
    def get_bought_title_by_address(cls, address, chain):
        client = cls.dynamodb_client
        filter_expression = {
            "FilterExpression": "#75860 = :75860 And #75861 = :75861 And #75862 = :75862 And NOT (#75863 = :75863)",
            "ExpressionAttributeNames": {"#75860":"jsrSent","#75861":"onSale","#75862":"accountAddr","#75863":"extCID"},
            "ExpressionAttributeValues": {":75860": {"BOOL": True},":75861": {"BOOL": False},":75862": {"S":f"{address}"},":75863": {"N":"45"}}
        }
        response = client.scan(
            TableName=getattr(settings, f"AWS_DYNAMODB_{chain.upper()}_TABLE_NAME"),
            **filter_expression
        )
        token_data = [cls.__getBoughtTokenJson(token) for token in response.get("Items")]
        result_data = cls.test_main_filter(chain.upper(), token_data)
        return result_data

    @classmethod
    def get_bought_title_by_address_before_date(cls, address, chain, date):
        client = cls.dynamodb_client
        filter_expression = {
            "FilterExpression": "#39240 = :39240 And #39241 = :39241 And NOT (#39242 = :39242) And #39243 = :39243 And #39244 < :39244",
            "ExpressionAttributeNames": {"#39240":"jsrSent","#39241":"onSale","#39242":"extCID","#39243":"accountAddr","#39244":"updatedAt"},
            "ExpressionAttributeValues": {":39240": {"BOOL": True},":39241": {"BOOL": False},":39242": {"N":"45"},":39243": {"S":f"{address}"},":39244": {"S":f"{date}"}}
        }

        response = client.scan(
            TableName=getattr(settings, f"AWS_DYNAMODB_{chain.upper()}_TABLE_NAME"),
            **filter_expression
        )
        token_data = [cls.__getBoughtTokenJson(token) for token in response.get("Items")]
        result_data = cls.test_main_filter(chain.upper(), token_data)
        return result_data

    @classmethod
    def get_total_bought_title(cls, chain):
        client = cls.dynamodb_client
        filter_expression = {
            "FilterExpression": "#75860 = :75860 And #75861 = :75861 And NOT (#75863 = :75863)",
            "ExpressionAttributeNames": {"#75860":"jsrSent","#75861":"onSale","#75863":"extCID"},
            "ExpressionAttributeValues": {":75860": {"BOOL": True},":75861": {"BOOL": False},":75863": {"N":"45"}}
        }
        response = client.scan(
            TableName=getattr(settings, f"AWS_DYNAMODB_{chain.upper()}_TABLE_NAME"),
            **filter_expression
        )
        token_data = [cls.__getBoughtTokenJson(token) for token in response.get("Items")]
        result_data = cls.test_main_filter(chain.upper(), token_data)
        return len(result_data)

    @classmethod
    def get_value_stock_by_date(cls, start_date, end_date, chain):
        start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        keyword = "test" if chain == "TESTNET" else "main"
        client = cls.dynamodb_client

        filter_expression = {
            "FilterExpression": "#e2030 < :e2030 And contains(#e2031, :e2031)",
            "ExpressionAttributeNames": {"#e2030":"createdAt","#e2031":"assetID"},
            "ExpressionAttributeValues": {":e2030": {"S":start_date_str},":e2031": {"S":keyword}}
        }
        response = client.scan(
            TableName=getattr(settings, f"AWS_DYNAMODB_{chain.upper()}_TABLE_NAME"),
            **filter_expression
        )

        total_tokenized_value = cls._total_tokenized_base_value(response["Items"])

        result = []
        while start_date <= end_date:
            start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
            new_start_date = start_date + timedelta(1)
            new_start_date_str = new_start_date.strftime("%Y-%m-%dT%H:%M:%S")
            filter_expression = {
                "FilterExpression": "#e2030 > :e2030 And contains(#e2031, :e2031) And #e2032 < :e2032",
                "ExpressionAttributeNames": {"#e2030":"createdAt","#e2031":"assetID","#e2032":"createdAt"},
                "ExpressionAttributeValues": {":e2030": {"S":start_date_str},":e2031": {"S":keyword},":e2032": {"S":new_start_date_str}}
            }
            response = client.scan(
                TableName=getattr(settings, f"AWS_DYNAMODB_{chain.upper()}_TABLE_NAME"),
                **filter_expression
            )

            total_tokenized_value = total_tokenized_value + cls._total_tokenized_base_value(response["Items"])
            result.append({
                "date": int(start_date.timestamp()),
                "value": round((total_tokenized_value * Constant.ANALYTICS_TOTAL_CAPITAL_UNLOCK_RATIO)/1000000, 4)
            })
            start_date = new_start_date

        return result

    @classmethod
    def get_title_details(cls, title_id, chain):
        client = cls.dynamodb_client
        filter_expression = {
            "FilterExpression": "#4ff40 = :4ff40",
            "ExpressionAttributeNames": {"#4ff40":"extCID"},
            "ExpressionAttributeValues": {":4ff40": {"N":f"{title_id}"}}
        }
        response = client.scan(
            TableName=getattr(settings, f"AWS_DYNAMODB_{chain}_TABLE_NAME"),
            **filter_expression
        )
        data = {}
        item = response.get("Items")[0] if response.get("Items") else {}
        for item_key, item_value in item.items():
            for key, value in item_value.items():
                data[item_key] = value
        if data.get("__typename"):
            data.pop("__typename")
        return data

class S3():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    @classmethod
    def uploadObject(cls, object, objectName):
        cls.s3_client.upload_fileobj(
            object, settings.AWS_STORAGE_BUCKET_NAME, objectName)
        return objectName

    @classmethod
    def uploadInBytes(cls, object, objectName):
        cls.s3_client.put_object(
            Body=object, Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=objectName)
        return objectName
