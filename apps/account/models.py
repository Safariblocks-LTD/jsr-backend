from django.db import models
from utils import (
    Cryptography,
    Generator,
    Responder, 
    Twilio,
)
from django.utils import timezone


class DeviceManager(models.Manager):
    
    def remove(self, **kwargs):
        if not kwargs.get("address"):
            self.filter(**kwargs).update(is_deleted=True)
        kwargs["device__fcm_token"] = kwargs.pop("fcm_token", None)
        return Account.objects.remove(**kwargs)

    def remove_by_fcm_token(self, fcm_token):
        self.filter(fcm_token=fcm_token).update(is_deleted=True)

    def get_by_fcm_token(self, token):
        return self.filter(fcm_token=token, is_deleted=False).first()
    
    def is_mobile_registered(self, mobile):
        return self.filter(mobile=mobile, is_deleted=False).exists()
    
    def get_by_mobile(self, mobile):
        country_code, mobile = mobile.split("_", 1)
        return self.get_by_country_code_and_number(country_code, mobile)
    
    def get_by_country_code_and_number(self, country_code, number):
        return self.filter(country_code=country_code, mobile=number, is_deleted=False).first()

    def get_by_fcm_and_mobile(self, fcm_token, mobile):
        country_code, mobile = mobile.split("_", 1)
        return self.filter(
            country_code=country_code, mobile=mobile, fcm_token=fcm_token, is_deleted=False
        ).first()

    def get_by_mobile_and_exclude_fcm_token(self, mobile, fcm_token):
        country_code, mobile = mobile.split("_", 1)
        return self.filter(mobile=mobile, country_code=country_code, is_deleted=False, is_wallet=True).exclude(fcm_token=fcm_token).first()

    def get_latest_by_mobile(self, mobile):
        country_code, mobile = mobile.split("_", 1)
        return self.filter(mobile=mobile, country_code=country_code, is_deleted=False).order_by("-id").first()



class Device(models.Model):
    fcm_token = models.TextField(null=True, blank=True)
    private_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mobile = models.CharField(null=True, max_length=25)
    country_code = models.CharField(null=True, max_length=10)
    requested_mobile = models.CharField(max_length=25, null=True)
    otp = models.CharField(max_length=6, null=True)
    otp_created_at = models.DateTimeField(null=True)
    otp_verification_attempt = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_wallet = models.BooleanField(default=False)
    objects = DeviceManager()
    
    class Meta:
        db_table = "devices"
        
    def update(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)
        self.save()
        
    def mobile_number(self):
        return f"{self.country_code}_{self.mobile}"
    
    def send_new_otp(self, requested_mobile):
        otp = Generator.generate_mobile_otp()
        self.update({
            "is_verified": False,
            "requested_mobile": requested_mobile,
            "otp": otp,
            "otp_created_at": timezone.now(),
            "otp_verification_attempt": 0
        })
        Twilio.send(requested_mobile.replace("_", "", 1), 100, otp=otp)
        
    def confirm(self):
        country_code, mobile = self.requested_mobile.split("_", 1)
        self.update({
            "country_code": country_code,
            "mobile": mobile,
            "requested_mobile": None,
            "otp": None,
            "otp_created_at": None,
            "otp_verification_attempt": 0,
            "is_verified": True
        })

    def confirm_wallet(self, fcm_token, presist_account):
        if not self.is_verified:
            Responder.raise_error(181)
        self.is_wallet = True
        self.fcm_token = fcm_token
        self.save()
        if not presist_account:
            Account.objects.filter(device=self.id).update(is_deleted=True)
        Account.objects.filter(device=self.id).update(is_imported=False, is_primary=False)

    def remove_mobile(self):
        self.update({"country_code": None, "mobile": None})


class AccountManager(models.Manager):
    def get_all_by_device_id(self, device_id):
        return self.filter(device_id=device_id, is_deleted=False)

    def get_all_imported_by_device_id(self, device_id):
        return self.filter(device_id=device_id, is_deleted=False, is_imported=True)

    def register(self, **kwargs):
        public_key, private_key = Cryptography.get_public_private_keys()
        address = kwargs.pop("address", None) 
        kwargs["is_deleted"] = False
        device, _ = Device.objects.update_or_create(**kwargs, defaults={"private_key":private_key})
        id = self._register(address=address, device=device)
        return public_key, id

    def _register(self, **kwargs):
        instance = self.filter(**kwargs).first()
        if not instance:
            instance = self.create(**kwargs)
        return instance.id            
        
    def remove(self, **kwargs):
        if instance := self.filter(**kwargs):
            return instance.update(is_deleted=True)
        Responder.raise_error(117)
        
    def get_devices_by_address(self, address):
        return [account.device for account in self.filter(address=address, is_deleted=False)]

    def get_devices_by_imported_address(self, address):
        return [account.device for account in self.filter(address=address, is_deleted=False, is_imported=True)]

    def get_sender_and_receiver_devices(self, sender_address, receiver_address):
        return self.get_devices_by_address(sender_address), self.get_devices_by_address(receiver_address)
    
    def get_account_by_id(self, id):
        return self.filter(id=id).first()

    def get_by_device_and_address(self, device_id, address):
        return self.filter(device_id=device_id, address=address, is_deleted=False).first()

    def get_primary_account(self, device_id):
        return self.filter(device_id=device_id, is_imported=True, is_primary=True, is_deleted=False)


class Account(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=150)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="account_device", default=None)
    is_deleted = models.BooleanField(default=False)
    is_imported = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    objects = AccountManager()

    class Meta:
        db_table = "accounts"
