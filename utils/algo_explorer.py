import httpx
import os
from utils import Constant
from django.core.cache import cache
from utils.logger import Logger


class AlgoExplorer:

    MAINNET_BASE_URL = Constant.ALGO_EXPLORER_MAINNET_BASE_URL
    TESTNET_BASE_URL = Constant.ALGO_EXPLORER_TESTNET_BASE_URL
    
    @classmethod
    def base_url(cls):
        return cls.MAINNET_BASE_URL if os.environ.get("ALGO_NET") == "mainnet" else cls.TESTNET_BASE_URL
    
    @classmethod
    def get_endpoint(cls, endpoint):
        return f"{cls.base_url()}/{endpoint}"
        
    @classmethod
    def get_account_info(cls, address):
        try:
            endpoint = cls.get_endpoint(f"accounts/{address}")
            account = httpx.get(endpoint)
            account = account.json().get("account")
            if not account.get("address"):
                raise
            account["assets"] = account.get("assets", [])
            account["assets"].insert(0, {
                "asset-id": 0,
                "amount": account["amount"],
                "name": "Algo",
                "unit-name": "ALGO",
                "verification": True
            })
            return account
        except Exception as e:
            Logger.custom_log(f"error: {e.args}")
            return cls.on_error_account_info(address)
            
    @classmethod
    def on_error_account_info(cls, address):
        return {
            "address": address,
            "amount": 0,
            "min-balance": Constant.MIN_TXN_FEE,
            "assets": [{
                "asset-id": 0,
                "amount": 0,
                "name": "Algo",
                "unit-name": "ALGO",
                "verification": True
            }],
            "total-assets-opted-in": 0,
        }
            
    @classmethod
    def get_txns(cls, **kwargs):
        try:
            kwargs["sort"] = "desc"
            if chain := kwargs.pop("chain", None):
                endpoint = f"{getattr(cls, f'{chain}_BASE_URL')}/transactions"
            else:
                endpoint = f"{cls.base_url()}/transactions"
            response = httpx.get(endpoint, params=kwargs)
            return response.json()
        except Exception as e:
            Logger.custom_log(f"error: {e.args}")
            return cls.on_error_txns()
        
    @classmethod
    def on_error_txns(cls):
        return {"transactions": []}
        
    @classmethod
    def get_assets(cls, **kwargs):
        try:
            endpoint = cls.get_endpoint("assets")
            response = httpx.get(endpoint, params=kwargs)
            return response.json()
        except Exception as e:
            Logger.custom_log(f"error: {e.args}")
            return cls.on_error_assets()
        
    @classmethod
    def on_error_assets(cls):
        return {"assets": []}
        
    @classmethod
    def asset_value_to_usd(cls, value, asset_id):
        if not value: return 0
        if asset_id in Constant.ASSETS_ID_SAME_VALUE_AS_USD:
            return value
        rate = cache.get(f"{asset_id}_2_USD")
        if not rate: 
            rate = cls.algo_to_usd()
            if asset_id:
                rate *= cls.asset_to_algo_rate(asset_id)
            cache.set(f"{asset_id}_2_USD", rate, 60*60)
        return round(rate * value, 6)
        
    @classmethod
    def algo_to_usd(cls):
        try:
            endpoint = Constant.ALGO_EXPLORER_ALGO_2_USD_URL
            return float(httpx.get(endpoint).json().get("price"))
        except Exception:
            return 0
        

    @classmethod
    def asset_id_to_unit_name(cls, asset_id, chain=None):
        """ Get asset unit name from asset ID."""
        if not asset_id:
            return {"unit_name": "ALGO",
                    "asset_name": "ALGO"}
        endpoint = cls.get_endpoint(f"assets/{asset_id}")
        if chain == "MAINNET":
            endpoint = cls.MAINNET_BASE_URL + f"/assets/{asset_id}"

        try:
            if not cache.get(endpoint):
                response = httpx.get(endpoint).json()["asset"]["params"]
                result = {"unit_name": response.get("unit-name", "UNNAMED"),
                        "asset_name": response.get("name", "Unnamed")}
                cache.set(endpoint, result, 7*60*60*24)
                return result
            return cache.get(endpoint)
        except Exception as e:
            Logger.custom_log(f"error: {e.args}")
            # If transaction does not have unit params, return an empty dict.
            return {}

    @classmethod
    def asset_detail_from_asset_id(cls, asset_id):
        if not asset_id:
            return {"unit-name": "ALGO",
                    "name": "ALGO"}
        endpoint = cls.get_endpoint(f"assets/{asset_id}")
        try:
            response = httpx.get(endpoint)
            response = response.json()["asset"]["params"]
            return response
        except Exception as e:
            Logger.custom_log(f"error: {e.args}")
            # If transaction does not have unit params, return an empty dict.
            return {}

    @classmethod
    def asset_to_algo_rate(cls, asset_id):
        try:
            query = {
                "type": "fixed-input",
                "amount": "10",
                "fromASAID": asset_id,
                "toASAID": 0,
                "algodUri": "https://node.testnet.algoexplorerapi.io",
                "algodToken": {},
                "algoPort": "",
                "chain": "testnet"
            }
            return httpx.get("https://api.deflex.fi/api/fetchQuote", params=query).json().get("priceBaseline") or 0
        except Exception:
            return 0