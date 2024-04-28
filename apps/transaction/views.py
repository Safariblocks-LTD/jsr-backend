from rest_framework.views import APIView
from .serializers import (
    TransactionSerializer,
    OfflineTransactionSerializer,
    TransactionListSerializer,
    TransactionExportListSerializer,
    TransactionListV2WalletSerializer,
    ProtocolTransactionSerializer,
    RequestTransactionSerializer,
    UpdateRequestTransactionSerializer,
    GetRequestTransactionSerializer
)
from jasiri_wallet.permissions import Public
from utils import (
    Validator,
    Responder, 
    Algorand, 
)
from apps.account.models import Account
from utils.aws import S3
from utils.helpers import Helper
import io
from .models import ProtocolTransaction, RequestTransaction
from django.conf import settings

class Transaction(APIView):
    
    def get(self, request, **kwargs):
        query_params = Validator.get_transaction_history_params(request)
        query_params["address"] = request.user.address
        txns = Algorand.get_txns_history(**query_params)
        txns = TransactionListSerializer(txns, context={"user":request.user}).data
        return Responder.send(106 if len(txns) else 110, txns)
    
    def post(self, request, **kwargs):
        serializer = TransactionSerializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(101)
    
    
class OfflineTransaction(APIView):
    permission_classes = (Public,)
    
    def post(self, request, **kwargs):
        serializer = OfflineTransactionSerializer(data=kwargs["data"])
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Responder.send(116)
        except Exception:
            return Responder.send(510)
        
    
class TwilioTransaction(OfflineTransaction):

    def post(self, request, **kwargs):
        kwargs["data"] = Validator.get_offline_txn_data(request.data, "From", "Body")
        return super().post(request, **kwargs)
    

class AfricasTalkingTransaction(OfflineTransaction):
    
    def post(self, request, **kwargs):
        kwargs["data"] = Validator.get_offline_txn_data(request.data, "from", "text")
        return super().post(request, **kwargs)
    


class ProtocolTransactionView(APIView):
    permission_classes = [Public]
    
    def get(self, request, **kwargs):
        page_no = int(request.GET.get('page_no', 1))
        items = int(request.GET.get('items', 20))
        start = (page_no-1)*items
        end = page_no*items
        search = request.GET.get("search")
        transactions = ProtocolTransaction.objects.get_all_transactions_by_search(search)
        length = len(transactions)
        transactions = transactions[start:end]
        serializers = ProtocolTransactionSerializer(transactions, many=True)
        return Responder.send(177, {"transactions":serializers.data,"length": length})

    def post(self, request, **kwargs):
        serializer = ProtocolTransactionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Responder.send(175, serializer.data)
        except:
            return Responder.raise_error(176)


class TransactionV2WalletView(APIView):
    permission_classes = [Public]

    def get(self, request, address, **kwargs):
        secondary_currency = request.query_params.get("secondary_currency", "USD")
        query_params = Validator.get_transaction_history_params(request)
        query_params["address"] = address
        Validator.validate_address(address)
        txns = []
        queryset = Account.objects.get_by_device_and_address(request.user.id, address)
        if queryset:
            txns = Algorand.get_txns_history(**query_params)
            txns = TransactionListV2WalletSerializer(
                txns, context={
                    "device": request.user, "secondary_currency": secondary_currency, "address": address
                }
            ).data
        return Responder.send(106 if len(txns) else 110, txns)


class ExportTransactionHistoryV2WalletView(APIView):
    permission_classes = [Public]

    def get(self, request, address, **kwargs):
        secondary_currency = request.query_params.get("secondary_currency", "USD")
        query_params = Validator.get_transaction_history_params(request)
        query_params["address"] = address
        Validator.validate_address(address)
        data = {}
        txns = []
        queryset = Account.objects.get_by_device_and_address(request.user.id, address)
        if queryset:
            txns = Algorand.get_txns_history(**query_params)
            txns = TransactionExportListSerializer(
                txns, context={"user": request.user, "secondary_currency": secondary_currency}
            ).data
            file = io.StringIO()
            fields = ["id", "note", "receiver", "sender", "txn_type", "asset_name", "asset_id", "total_amount", f"total_amount_in_{secondary_currency}"]
            file = Helper.write_csv(file, fields, txns["transactions"])
            endpoint = f"transactions/transaction_details_{request.user.id}.csv"
            S3().uploadInBytes(file.getvalue().encode(), f"transactions/transaction_details_{request.user.id}.csv")
            data["url"] = settings.BASE_CDN_URL + endpoint
        return Responder.send(200 if len(txns) else 110, data)


class RequestTransactionWalletV2View(APIView):
    permission_classes = (Public,)

    def post(self, request, **kawrgs):
        serializer = RequestTransactionSerializer(data=request.data, context={"device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(196, serializer.data)


class UpdateRequestTransactionWalletV2View(APIView):
    permission_classes = (Public,)

    def patch(self, request, pk, **kawrgs):
        request_transaction = RequestTransaction.objects.get_by_id(pk)
        if not request_transaction:
            Responder.raise_error(197)
        serializer = UpdateRequestTransactionSerializer(request_transaction, data=request.data, context={"device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(198, serializer.data)
