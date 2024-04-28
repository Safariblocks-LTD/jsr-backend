from django.db import models
from django.utils import timezone


class ProtocolTransactionManager(models.Manager):
    def get_all_transactions_by_search(self,search=None):
        if search:
            return self.filter(title_id__icontains=search).order_by('-id')
        return self.all().order_by('-id')
    

class ProtocolTransaction(models.Model):
    tx_id = models.CharField(max_length=100)
    title_id = models.CharField(max_length=20)
    activity = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    date = models.DateTimeField(null=False, default=timezone.now)

    objects = ProtocolTransactionManager()

    def __str__(self) -> str:
        return f"{self.title_id} {self.account}"

    class Meta:
        db_table = "protocol_transactions"


class RequestTransactionManager(models.Manager):
    def get_by_id(self, id):
        return self.filter(id=id).first()


class RequestTransaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    from_address = models.CharField(max_length=150)
    to_address = models.CharField(max_length=150)
    asset_id = models.IntegerField()
    asset_name = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255)
    amount = models.FloatField()
    is_rejected = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_request_resolved = models.BooleanField(default=False)
    device = models.ForeignKey('account.device', on_delete=models.CASCADE, related_name="request_transaction_device", default=None)

    objects = RequestTransactionManager()

    class Meta:
        db_table = "request_transactions"

    def update(self, details):
        for key in details:
            setattr(self, key, details[key])
        self.save()
        return self
