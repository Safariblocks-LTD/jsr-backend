import os
from .algorand import Algorand
from .constants import Constant
from celery import shared_task
from apps.account.models import Account
from apps.notification.models import Notification
from utils.algo_explorer import AlgoExplorer
from datetime import timedelta
from utils.helpers import Helper


@shared_task
def send_push_notifications(txn):
    devices = Account.objects.get_devices_by_imported_address(txn["sender"])
    if txn["txn_type"] == "optin_axfer":
        return Notification.objects.notify(devices, 103, txn)
    if txn["txn_type"] == "closeout_axfer":
        return Notification.objects.notify(devices, 104, txn)
    Notification.objects.create_and_notify(devices, 101, txn)
    if txn["sender"] != txn["receiver"]:
        devices = Account.objects.get_devices_by_imported_address(txn["receiver"])
        Notification.objects.create_and_notify(devices, 102, txn)


def fetch_txns(chain):
    kwargs = {"chain": chain}

    if os.environ.get(f"{chain}_LAST_TXN_ROUND"):
        try:
            start_round = int(os.environ.get(f"{chain}_LAST_TXN_ROUND")) + 1
        except Exception:
            start_round = Algorand.get_last_round(**kwargs) - 1
    else:
        start_round = Algorand.get_last_round(**kwargs) - 1

    kwargs["min-round"] = start_round

    accounts = Account.objects.filter(is_imported=True, is_deleted=False).distinct().values_list("address", flat=True)
    txns = Algorand.get_txns_history(**kwargs)
    for txn in txns.get("transactions"):
        txn["net_type"] = getattr(Constant, f"{chain}_CODE")
        if txn["sender"] in accounts or txn["receiver"] in accounts:
            if txn.get("asset_id"):
                txn["asset_name"] = AlgoExplorer.asset_id_to_unit_name(txn["asset_id"], chain).get("unit_name")
            send_push_notifications.delay(txn)
    os.environ[f"{chain}_LAST_TXN_ROUND"] = str(txns.get("current-round")) if txns.get("current-round") else str(start_round)


@shared_task(name="fetch_testnet_txns", queue="testnet_txn")
def fetch_testnet_txns():
    fetch_txns("TESTNET")


@shared_task(name="fetch_mainnet_txns", queue="mainnet_txn")
def fetch_mainnet_txns():
    fetch_txns("MAINNET")
