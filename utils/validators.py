from .algorand import Algorand
from .responder import Responder
from .helpers import Helper
from algosdk.encoding import is_valid_address
import datetime
from dateutil.relativedelta import relativedelta


class Validator:

    @staticmethod
    def get_transaction_history_params(request):
        try:
            query = {}
            if (request.query_params.get("from") and request.query_params.get("to")):
                query["after-time"] = Helper.rfc3339_datetime(
                    int(request.query_params.get("from")))
                query["before-time"] = Helper.rfc3339_datetime(
                    int(request.query_params.get("to")))
            if request.query_params.get("limit"):
                query["limit"] = int(request.query_params.get("limit"))
            if request.query_params.get("next_page_token"):
                query["next"] = request.query_params["next_page_token"]
            if request.query_params.get("duration") and request.query_params.get("timestamp"):
                before_time = Helper.rfc3339_datetime(
                    int(request.query_params.get("timestamp")))
                before_time = datetime.datetime.strptime(before_time, "%Y-%m-%d")
                if request.query_params.get("duration") == "month":
                    query["after-time"] = datetime.date(before_time.year, before_time.month, 1)
                if request.query_params.get("duration") == "quarter":
                    month = Helper.get_quarter_start_month(before_time.month)
                    query["after-time"] = datetime.date(before_time.year, month, 1)
                if request.query_params.get("duration") == "year":
                    query["after-time"] = datetime.date(before_time.year, 1, 1)
                query["after-time"] = query["after-time"] - relativedelta(days=1)
                query["after-time"] = query["after-time"].strftime("%Y-%m-%d")
            return query
        except Exception:
            Responder.raise_error(107)

    @classmethod
    def get_all_assets_queryparams(cls, request):
        query = {}
        if request.query_params.get("next_page_token"):
            query["next"] = request.query_params["next_page_token"]
        if search_text := request.query_params.get("search_text"):
            try:
                query["asset-id"] = int(search_text)
            except Exception:
                query["name"] = search_text
        return query

    @classmethod
    def validate_data_for_offline_transactions(cls, data):
        keys = {"pk", "adrs", "amt", "note", "iat"}
        try:
            if not data.keys() >= keys:
                raise
            # if Helper.is_timestamp_over(int(data["iat"]), Constant.OFFLINE_TXN_EXPIRE_TIME):
                # raise
            return {
                "sender": Algorand.get_address_from_private_key(data["pk"]),
                "sender_pk": data["pk"],
                "receiver": data["adrs"],
                "amt": int(data["amt"]),
                "note": data["note"],
            }
        except Exception:
            Responder.raise_error(510)

    @classmethod
    def validate_mobile(cls, mobile):
        import phonenumbers
        from phonenumbers.phonenumberutil import region_code_for_country_code
        region_code, mobile = mobile.split("_", 1)
        try:
            number = phonenumbers.parse(f"{region_code} {mobile}")
            if not phonenumbers.is_valid_number_for_region(
                    number, region_code_for_country_code(number.country_code)):
                raise
        except Exception:
            Responder.raise_error(127)
            
    @classmethod
    def get_offline_txn_data(cls, data, key1, key2):
        if not (data.get(key1) and data.get(key2)):
            Responder.raise_error(510)
        return {"sender": data[key1], "message": data[key2]}
    
    @classmethod
    def validate_address(cls, address):
        if not is_valid_address(address):
            Responder.raise_error(100)
