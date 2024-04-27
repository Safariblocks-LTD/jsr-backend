from datetime import datetime,timedelta
from base64 import b64decode
from algosdk.util import microalgos_to_algos
from .algo_explorer import AlgoExplorer
from django.utils import timezone as django_timezone
from bs4 import BeautifulSoup
import requests
from django.core.cache import cache
from django.conf import settings
from jwt import encode, decode
from .responder import Responder
import random
from .constants import Constant
from apps.asset.models import TickerNameData, DevicePriceData, AssetMaintenanceStatus
import csv
from utils.logger import Logger
from utils.aws import Dynamodb

class Helper:
    
    @classmethod
    def rfc3339_datetime(cls, timestamp):
        if timestamp is None:
            return None
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

    @classmethod
    def get_quarter_start_month(cls, month):
        quarter = (month-1) // 3
        return (quarter * 3) + 1

    @classmethod
    def is_time_over(cls, datetime, minutes):
        return datetime.timestamp() + 60*minutes < django_timezone.now().timestamp()
    
    @classmethod
    def is_timestamp_over(cls, timestamp, minutes):
        return timestamp + 60*minutes < django_timezone.now().timestamp()
    
    @classmethod
    def decode(cls, text):
        return b64decode(text) if text else None
    
    @classmethod
    def amount_in_algo(cls, number):
        return float(microalgos_to_algos(number))
    
    @classmethod
    def microamount_in_algo_usd(cls, amount, asset_unit="ALGO", asset_id=0, secondary_currency="USD"):
        amount = cls.amount_in_algo(amount)
        if asset_id in [487086338, 881424020]:
            return {
                "primary": {
                    "currency": asset_unit,
                    "value": round(amount, 6),
                },
                "secondary": {
                    "currency": secondary_currency,
                    "value": round(float(amount)*cls.get_asset_value_to_currency('USD', secondary_currency), 6),
                }
            }
        return {
            "primary": {
                "currency": asset_unit,
                "value": round(amount, 6),
            },
            "secondary": {
                "currency": secondary_currency,
                "value": round(float(amount)*cls.get_asset_value_to_currency(asset_unit, secondary_currency), 6),
            }
        }

    @classmethod
    def get_asset_value_to_currency(cls, asset_unit="ALGO", currency='USD'):
        if not asset_unit:
            asset_unit = "UNNAMED"
        rate = 0
        if cache.get(f"{asset_unit}_to_{currency}") == "NOT FOUND":
            return rate
        if not cache.get(f"{asset_unit}_to_{currency}"):
            url = f"https://api.coinbase.com/v2/prices/{asset_unit.upper()}-{currency.upper()}/spot"
            resp = requests.get(url)
            if resp.status_code != 200:
                cache.set(f"{asset_unit}_to_{currency}", "NOT FOUND", 30*60)
                return 0
            rate = resp.json().get('data').get('amount')
            cache.set(f"{asset_unit}_to_{currency}", float(rate), 30*60)
        return float(cache.get(f"{asset_unit}_to_{currency}"))

  
    @classmethod
    def get_total_amount(cls, txn, asset_id):
        asset_value = txn["amount"]["primary"]["value"]
        if asset_value and asset_id:
            asset_value *= AlgoExplorer.asset_to_algo_rate(asset_id)
        return {
            "primary": {
                "currency": "ALGO",
                "value": txn["fee"]["primary"]["value"] + asset_value,
            },
            "secondary": {
                "currency": "USD",
                "value": txn["fee"]["secondary"]["value"] + txn["amount"]["secondary"]["value"]
            }
        }
        
    
    @classmethod
    def get_short_name(cls, name):
        if name is None:
            return "UNN"
        name_list = name.split()
        name = name if len(name_list)==1 else "".join([name_[0] for name_ in name_list])
        return name[:3].upper()
    
    @classmethod
    def get_country_code_and_number(cls, mobile_number):
        import phonenumbers
        mobile_number = phonenumbers.parse(mobile_number)
        return f"+{mobile_number.country_code}", str(mobile_number.national_number)
    
    @classmethod
    def pay_transaction_parser(cls, transaction):
        """
        Algo Transaction
        """
        return {
            "id": transaction["id"],
            "timestamp": transaction["round-time"] * 1000,
            "fee": transaction["fee"],
            "amount": Helper.amount_in_algo(transaction["payment-transaction"]["amount"]),
            "note": transaction.get("note",""),
            "receiver": transaction["payment-transaction"]["receiver"],
            "sender": transaction["sender"],
            "txn_type": transaction["tx-type"],
            "asset_name": "ALGO"
        }
    
    @classmethod
    def axfer_transaction_parser(cls, transaction, chain=None):
        """
        Asset Transfer Transaction
        """
        asset_name = None
        if not chain:
            asset_name = AlgoExplorer.asset_id_to_unit_name(transaction["asset-transfer-transaction"]["asset-id"], chain).get("unit_name")
        return {
            "id": transaction["id"],
            "timestamp": transaction["round-time"] * 1000,
            "fee": transaction["fee"],
            "amount": Helper.amount_in_algo(transaction["asset-transfer-transaction"]["amount"]),
            "receiver": transaction["asset-transfer-transaction"]["receiver"],
            "sender": transaction["sender"],
            "note": transaction.get("note",""),
            "asset_id": transaction["asset-transfer-transaction"]["asset-id"],
            "close_amount": transaction["asset-transfer-transaction"]["close-amount"],
            "close_to": transaction["asset-transfer-transaction"].get("close-to"),
            "txn_type": transaction["tx-type"],
            "asset_name": asset_name
        }
        
    @classmethod
    def appl_transactions_parser(cls, transaction):
        """
        Application Transaction
        """
        pass
        
    @classmethod
    def parse_transaction(cls, transaction, chain=None):
        """
        "pay", "keyreg", "acfg", "axfer", "afrz"
        """
        if transaction["tx-type"] == "pay":
            return cls.pay_transaction_parser(transaction)
        if transaction["tx-type"] == "axfer":
            return cls.axfer_transaction_parser(transaction, chain)
            
            
    @classmethod
    def bytes_encoder(cls, string):
        return bytes(string, 'utf-8') if string else None
    
    @classmethod
    def get_asset_from_assets_by_index(cls, assets, index):
        return next((asset for asset in assets if asset["asset-id"] == index), None)
    
    @classmethod
    def get_txn_in_short(cls, txn):
        return {
            "id": txn["id"],
            "txn_type": txn["txn_type"],
            "asset_name": txn["asset_name"],
            "asset_id": txn.get("asset_id", 0),
            "amount": txn["amount"],
            "sender": txn["sender"],
            "receiver": txn["receiver"]
        }
        
    @classmethod
    def get_address_in_short(cls, adrs):
        return f"{adrs[:6]}....{adrs[-4:]}"
    
    @staticmethod
    def getSoup(url):
        headers = {
            "User-Agent": random.choice(Constant.userAgents)
        }
        return BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    
    @staticmethod
    def getCachedData(key):
        return cache.get(key)
    
    @staticmethod
    def setCacheData(key, data):
        ttl_minutes = int(settings.NEWS_TTL_MINUTES)
        ttl_seconds = ttl_minutes * 60
        return cache.set(key, data, timeout=ttl_seconds)      
    
    @staticmethod
    def deleteCacheData(key):
        return cache.delete(key)

    @classmethod
    def encode_jwt_token(cls, payload):
        payload["exp"] = django_timezone.now() + django_timezone.timedelta(days=settings.JWT_EXPIRATION_DAYS)
        return encode(payload, settings.SECRET_KEY, 'HS256')
    
    @classmethod
    def jwt_decode(cls, access_token):
        try:
            payload = decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            Responder.raise_error(513)
        return payload

    @classmethod
    def transaction_time_date(cls, timestamp):
        timestamp_datetime = datetime.fromtimestamp(timestamp / 1000)
        formatted_time = timestamp_datetime.strftime("%H:%M-%m/%d/%Y")
        return formatted_time
    
    @classmethod
    def get_device_details(cls, user_agent):
        api_key = settings.USERSTACK_KEY
        api_url = f'http://api.userstack.com/detect?access_key={api_key}&ua={user_agent}'
        response = requests.get(f'{api_url}')
        response = response.json() if response.status_code == 200 else None
        return response
    
    @classmethod
    def get_ticker_name(cls, brand, category):
        category_id = Constant.deviceCategories.get(category.lower())
        ticker_name = TickerNameData.objects.get_ticker_name(brand, category_id)
        return ticker_name
    
    
    @classmethod
    def convert_premium_to_selected_currency(self, premium, currency):
        url = f"https://api.coinbase.com/v2/prices/USD-{currency.upper()}/spot"
        resp = requests.get(url)
        rate = resp.json().get('data').get('amount')
        premium = float(premium) * float(rate)
        premium = round(premium, 6)
        return premium
    

    @classmethod
    def generate_passcode(self):
        return str(random.randint(100000, 999999))
    

    @classmethod
    def round_asset_count_to_decimal(self, number):
        if number:
            return round(number/1000000,6)
        return 0

    @classmethod
    def write_csv(cls, file, fields, data):
        csv_file = csv.DictWriter(file, fieldnames=fields)
        csv_file.writeheader()
        csv_file.writerows(data)
        return file

    @classmethod
    def percent_24h_change_currency(cls, currency='ALGORAND', secondary_currency='USD'):
        currency = currency.lower()
        secondary_currency = secondary_currency.lower()
        rate = {}
        try:
            if not cache.get(f"{currency}_to_{secondary_currency}_24h_change"):
                resp = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={currency}&vs_currencies={secondary_currency}&include_24hr_change=true")
                rate = resp.json().get(f"{currency}").get(f"{secondary_currency}_24h_change")
                cache.set(f"{currency}_to_{secondary_currency}_24h_change", rate, 5*60)
            rate = cache.get(f"{currency}_to_{secondary_currency}_24h_change")
        except Exception:
            return 0
        return rate if rate else 0

    @classmethod
    def get_asset_graph_data(cls, asset_name="ALGORAND", secondary_currency="USD"):
        asset_name = asset_name.lower()
        secondary_currency = secondary_currency.lower()
        if cache.get(f"{asset_name}_{secondary_currency}_graph") == "NOT FOUND":
            return {}
        if not (graph_data := cache.get(f"{asset_name}_{secondary_currency}_graph")):
            resp = requests.get(f"https://api.coingecko.com/api/v3/coins/{asset_name}/market_chart?vs_currency={secondary_currency}&days=90&interval=daily&precision=4")
            if resp.status_code != 200:
                cache.set(f"{asset_name}_{secondary_currency}_graph", "NOT FOUND", 24*60*60)  # caching for a day
                return {}
            graph_data = resp.json()
            cache.set(f"{asset_name}_{secondary_currency}_graph", graph_data, 24*60*60)  # caching for a day
        return graph_data

    @classmethod
    def get_portfolio_percentage(cls, total_algo, total_amount, secondary_currency):
        current_portfolio = total_algo + total_amount
        percentage_change = cls.percent_24h_change_currency("algorand", secondary_currency)
        prev_portfolio = total_amount + (total_algo*100/(100 + percentage_change))
        divisor = prev_portfolio
        if divisor == 0:
            divisor = 1
        percentage = (current_portfolio - prev_portfolio) * 100 / divisor
        return percentage
