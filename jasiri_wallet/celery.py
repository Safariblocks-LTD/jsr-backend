import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jasiri_wallet.settings")
os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

app = Celery("jasiri_wallet")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
    
app.conf.beat_schedule = {
    "fetch-testnet-txns": {
        "task": "fetch_testnet_txns",  
        "schedule": 5.0,
    },
    "fetch-mainnet-txns": {
        "task": "fetch_mainnet_txns",  
        "schedule": 5.0,
    },
}  