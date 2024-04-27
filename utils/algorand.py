import os
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk.transaction import (
    PaymentTxn,
    AssetOptInTxn,
    AssetCloseOutTxn,
    AssetTransferTxn,
)
from algosdk.mnemonic import to_private_key
from algosdk import account
from django.conf import settings
from base64 import b64decode
from .responder import Responder
from .helpers import Helper
from .algo_explorer import AlgoExplorer
from django.conf import settings


class Algorand():
    
    ALGO_TOKEN = settings.ALGO_TOKEN
    TESTNET_ALGOD_CLIENT = settings.TESTNET_ALGO_ENDPOINT
    TESTNET_INDXR_CLIENT = settings.TESTNET_ALGO_INDEXER_ENDPOINT
    MAINNET_ALGOD_CLIENT = settings.MAINNET_ALGO_ENDPOINT
    MAINNET_INDXR_CLIENT = settings.MAINNET_ALGO_INDEXER_ENDPOINT
    
    testnet_algod_client = AlgodClient(ALGO_TOKEN, TESTNET_ALGOD_CLIENT, {"X-API-Key": ALGO_TOKEN})
    testnet_indexer_client = IndexerClient(ALGO_TOKEN, TESTNET_INDXR_CLIENT, {"X-API-Key": ALGO_TOKEN})
    mainnet_algod_client = AlgodClient(ALGO_TOKEN, MAINNET_ALGOD_CLIENT, {"X-API-Key": ALGO_TOKEN})
    mainnet_indexer_client = IndexerClient(ALGO_TOKEN, MAINNET_INDXR_CLIENT, {"X-API-Key": ALGO_TOKEN})


    @classmethod
    def get_algod_client(cls):
        if settings.SERVER.lower() == "prod":
            return cls.mainnet_algod_client
        else:
            return cls.testnet_algod_client
    

    @classmethod
    def __algod_client(cls, **kwargs):
        if chain := kwargs.get("chain"):
            return getattr(cls, f"{chain.lower()}_algod_client")
        return getattr(cls, f"{os.environ.get('ALGO_NET', 'testnet')}_algod_client")
    
    @classmethod
    def get_address_from_private_key(cls, private_key):
        try:
            return account.address_from_private_key(private_key)
        except Exception:
            Responder.raise_error(507)  
            
    @classmethod
    def get_private_key_from_mnemonic_b64(cls, mnemonic):
        try:
            return to_private_key(b64decode(mnemonic).decode())
        except Exception:
            Responder.raise_error(511)   
    
    @classmethod
    def get_account_info(cls, address):
        return AlgoExplorer.get_account_info(address)
    
    @classmethod
    def transactions(cls, sender_pk, **attrs):
        txn_type = attrs.pop("txn_type")
        attrs["sp"] = cls.__algod_client().suggested_params()
        
        if txn_type == "pay":
            txn = PaymentTxn(**attrs)
        elif txn_type == "axfer":
            txn = AssetTransferTxn(**attrs)
        elif txn_type == "optin_axfer":
            txn = AssetOptInTxn(**attrs)
        elif txn_type == "closeout_axfer":
            txn = AssetCloseOutTxn(**attrs)
            
        try:
            signed_txn = txn.sign(sender_pk)
            cls.__algod_client().send_transaction(signed_txn)
        except Exception as e:
            Responder.raise_error(134, error=str(e).split(":")[-1].strip())
    
    @classmethod
    def get_txns_history(cls, **kwargs):
        txns = AlgoExplorer.get_txns(**kwargs)
        chain = [kwargs.get("chain")] * len(txns["transactions"])
        txns["transactions"] = list(filter(lambda txn: txn, map(Helper.parse_transaction, txns["transactions"], chain)))
        return txns
    
    @classmethod
    def get_all_assets(cls, **kwargs):
        return AlgoExplorer.get_assets(**kwargs)
    
    @classmethod
    def get_last_round(cls, **kwargs):
        return cls.__algod_client(**kwargs).status().get("last-round")