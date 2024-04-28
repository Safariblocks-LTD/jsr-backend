from rest_framework import serializers
from utils import (
    Cryptography,
    Responder,
    Validator, 
    Constant,
    Algorand, 
    Helper, 
    FCM,
)
from apps.account.models import Device, Account
import os
import base64
import json
from .models import ProtocolTransaction, RequestTransaction
from django.db.models import Q


class TransactionSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=255)
    amt = serializers.IntegerField()
    note = serializers.CharField(required=False)
    index = serializers.IntegerField(required=False)
    txn_type = serializers.ChoiceField(choices=Constant.TXN_CHOICES)
    
    def validate(self, attrs):
        if attrs["txn_type"] == "pay":
            attrs.pop("index", None)
        if attrs["txn_type"] == "axfer" and not attrs.get("index"):
            Responder.raise_error(506)
        return attrs
    
    def create(self, attrs):
        attrs["note"] = Helper.bytes_encoder(attrs.get("note"))
        attrs["sender"] = self.context["user"].address
        Algorand.transactions(self.context["user"].private_key, **attrs)
        return {}


class TransactionDetailSerializer(serializers.Serializer):

    def to_representation(self, txn):
        currency = self.context.get("currency", "USD")
        txn["status"] = 1
        txn["fee"] = Helper.microamount_in_algo_usd(txn["fee"], secondary_currency=currency)
        asset_id = txn.get("asset_id", 0)
        txn["amount"] = Helper.microamount_in_algo_usd(
            txn["amount"] * pow(10, 6), txn["asset_name"], asset_id, secondary_currency=currency)
        txn["total_amount"] = Helper.get_total_amount(txn, asset_id)
        return txn


class TransactionListSerializer(serializers.Serializer):

    def to_representation(self, instance):
        secondary_currency = self.context.get("secondary_currency", "USD")
        response = {
            "transactions": TransactionDetailSerializer(
                instance["transactions"],
                context={"user": self.context["user"], "currency": secondary_currency},
                many=True
            ).data,
        }
        if instance.get("next-token"):
            response["next_page_token"] = instance["next-token"]
        return response


class OfflineTransactionSerializer(serializers.Serializer):

    message = serializers.CharField()
    sender = serializers.CharField()
    
    def validate(self, attrs):
        device = Device.objects.get_by_country_code_and_number(*Helper.get_country_code_and_number(attrs["sender"]))
        if not device:
            Responder.raise_error(510)
        FCM.validate(device.fcm_token)
        attrs = Cryptography.decrypt(attrs["message"], device.private_key)
        os.environ["ALGO_NET"] = attrs.get("net_type", "testnet")
        attrs = Validator.validate_data_for_offline_transactions(attrs)
        return attrs
    
    def create(self, attrs):
        attrs["txn_type"] = "pay"
        Algorand.transactions(attrs.pop("sender_pk"), **attrs)
        return {}
    

class ProtocolFeedDetailSerializer(serializers.Serializer):
    def to_representation(self, txn):
        feed = {}
        feed['originator_account'] = txn['sender']
        feed['time_stamp'] = Helper.transaction_time_date(txn['timestamp'])
        if note := base64.b64decode(txn.get("note", "")).decode("utf-8"):
            feed["title_id"] = json.loads(note).get("title_id") if note else None
            feed["activity"] = json.loads(note).get("activity") if note else None
        feed["algoexplorer"] = f"https://{self.context['chain']}.algoexplorer.io/tx/{txn['id']}"
        return feed


class ProtocolTransactionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProtocolTransaction
        fields = ["tx_id", "title_id", "activity", "account", "date"]


class TransactionExportListSerializer(serializers.Serializer):

    def to_representation(self, instance):
        secondary_currency = self.context.get("secondary_currency", "USD")
        response = {
            "transactions": TransactionExportDetailSerializer(
                instance["transactions"],
                context={"user": self.context["user"], "currency": secondary_currency},
                many=True
            ).data,
        }
        if instance.get("next-token"):
            response["next_page_token"] = instance["next-token"]
        return response


class TransactionExportDetailSerializer(serializers.Serializer):

    def to_representation(self, txn):
        currency = self.context.get("currency", "USD")
        txn["fee"] = Helper.microamount_in_algo_usd(txn["fee"], secondary_currency=currency)

        asset_id = txn.get("asset_id", 0)
        txn["amount"] = Helper.microamount_in_algo_usd(
            txn["amount"] * pow(10, 6), txn["asset_name"], asset_id, secondary_currency=currency)

        txn["total_amount"] = Helper.get_total_amount(txn, asset_id)
        txn[f"total_amount_in_{currency}"] = txn["total_amount"]["secondary"]["value"]
        txn["total_amount"] = txn["total_amount"]["primary"]["value"]

        txn.pop('amount')
        txn.pop('fee')
        txn.pop("timestamp")

        if "close_amount" in txn.keys():
            txn.pop("close_amount")
        if "close_to" in txn.keys():
            txn.pop("close_to")

        return txn


class RequestTransactionSerializer(serializers.Serializer):
    from_address = serializers.CharField(max_length=150)
    to_address = serializers.CharField(max_length=150)
    asset_id = serializers.IntegerField()
    asset_name = serializers.CharField(max_length=255)
    transaction_type = serializers.CharField(max_length=255)
    amount = serializers.FloatField()

    def validate(self, attrs):
        Validator.validate_address(attrs.get("from_address"))
        Validator.validate_address(attrs.get("to_address"))
        if not Account.objects.get_by_device_and_address(self.context["device"].id, attrs.get("from_address")):
            Responder.raise_error(117)
        attrs["device"] = self.context["device"]
        return attrs

    def create(self, attrs):
        return RequestTransaction.objects.create(**attrs)


class UpdateRequestTransactionSerializer(serializers.Serializer):
    is_rejected = serializers.BooleanField(required=False)
    is_approved = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if attrs.get("is_rejected") and attrs.get("is_approved"):
            Responder.raise_error(505)
        attrs["is_request_resolved"] = True
        return attrs

    def update(self, instance, attrs):
        if instance.is_request_resolved:
            Responder.raise_error(199)
        instance.update(attrs)
        return {}


class TransactionListV2WalletSerializer(serializers.Serializer):

    def to_representation(self, instance):
        secondary_currency = self.context.get("secondary_currency", "USD")
        response = {
            "transactions": TransactionDetailSerializer(
                instance["transactions"],
                context={"user": self.context["device"], "currency": secondary_currency},
                many=True
            ).data,
        }

        requested_txns = RequestTransaction.objects.filter(
            to_address=self.context["address"], is_request_resolved=False
        ).order_by("-created_at")
        response["request_txns"] = GetRequestTransactionSerializer(
            requested_txns, context={"device": self.context["device"]}, many=True
        ).data

        pending_txns = RequestTransaction.objects.filter(
            from_address=self.context["address"], is_request_resolved=False
        ).order_by("-created_at")
        pending_txns = GetRequestTransactionSerializer(
            pending_txns, context={"device": self.context["device"]}, many=True
        ).data
        for txn in pending_txns:
            txn["transaction_type"] = "pending"
        response["request_txns"].extend(pending_txns)

        if instance.get("next-token"):
            response["next_page_token"] = instance["next-token"]
        return response


class GetRequestTransactionSerializer(serializers.ModelSerializer):
    created_at_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = RequestTransaction
        fields = [
            "id", "from_address", "to_address", "asset_id",
            "asset_name", "transaction_type", "amount", "created_at",
            "created_at_timestamp"
        ]
        read_only_fields = ["id"]

    def get_created_at_timestamp(self, instance):
        return int(instance.created_at.timestamp()) * 1000 if instance.created_at else None
