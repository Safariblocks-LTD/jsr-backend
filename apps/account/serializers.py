from rest_framework import serializers
from utils import (
    Responder,
    Validator,
    Algorand,
    Constant,
    Helper, 
    FCM, 
)
from .models import (
    Account, 
    Device,
)
from apps.asset.serializers import MyAssetDetailSerializer
from jwt import encode
from django.conf import settings
from utils.cryptography import Cryptography
from utils.contact import Contact
import bcrypt


class JWTAccountRegistrationSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)
    fcm_token = serializers.CharField()

    def validate(self, attrs):
        Validator.validate_address(attrs['address'])
        if bcrypt.hashpw(
            bytes(attrs['address'], encoding="utf-8"),
            bytes("$" + settings.BCRYPT_SALT, encoding="utf-8"),
        ) != bytes(attrs['fcm_token'], encoding="utf-8"):
            Responder.raise_error(206)
        return attrs

    def create(self, attrs):
        _, id = Account.objects.register(**attrs)
        payload = {
            "account_id":id
        }
        return {"token": Helper.encode_jwt_token(payload)}


class AccountDetailSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)
    
    def to_representation(self, instance):
        return {
            "address": instance["address"],
            "amount": Helper.microamount_in_algo_usd(instance["amount"], secondary_currency="$"),
            "min_balance":0.1*len(instance.get("assets", [])),
            "assets": MyAssetDetailSerializer(instance["assets"], many=True).data,
            "total_assets": instance["total-assets-opted-in"],
        }
    
    
class AccountRegistrationSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()
    mnemonic = serializers.CharField()

    def validate(self, attrs):
        attrs["private_key"] = Algorand.get_private_key_from_mnemonic_b64(attrs.pop("mnemonic"))
        attrs["address"] = Algorand.get_address_from_private_key(attrs["private_key"])
        FCM.validate(attrs["fcm_token"])
        return attrs
    
    def create(self, attrs):
        private_key = attrs.pop('private_key')
        rsa_public_key, _ = Account.objects.register(**attrs)
        return {
            "private_key": private_key,
            "rsa_public_key": rsa_public_key,
        }
        
        
class AccountRemoveSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()
    
    def validate(self, attrs):
        FCM.validate(attrs["fcm_token"])
        return attrs
    
    def create(self, attrs):
        Device.objects.remove(**attrs)
        return {}
    
    
class AccountMobileSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()
    mobile = serializers.CharField()
    otp = serializers.CharField(required=False, max_length=6)
    confirm = serializers.BooleanField(default=False)
    
    def validate(self, attrs):
        Validator.validate_mobile(attrs["mobile"])
        FCM.validate(attrs["fcm_token"])
        device = Device.objects.get_by_fcm_token(attrs["fcm_token"])
        if not device:
            Responder.raise_error(117)
        if device.mobile_number() == attrs["mobile"]:
            Responder.raise_error(118)
        if attrs.get("otp"):
            if device.requested_mobile != attrs["mobile"]:
                Responder.raise_error(124)
            if Helper.is_time_over(device.otp_created_at, Constant.OTP_EXPIRE_TIME):
                Responder.raise_error(122)
            if device.otp != attrs["otp"]:
                Responder.raise_error(123)
            if old_devices := Device.objects.get_by_mobile(device.requested_mobile):
                if not attrs.get("confirm"):
                    Responder.raise_error(121)
                old_devices.remove_mobile()
        elif device.otp_verification_attempt == Constant.OTP_MAX_ATTEMPTS:
            if not Helper.is_time_over(device.otp_created_at, Constant.OTP_MAX_ATTEMPTS_TIMEOUT):
                Responder.raise_error(119)
        elif device.otp_created_at and not Helper.is_time_over(device.otp_created_at, Constant.OTP_RESEND_TIMEOUT):
            Responder.raise_error(126)
        attrs["device"] = device
        return attrs
    
    def create(self, attrs):
        if attrs.get("otp"):
            attrs["device"].confirm()  
            return {
                "code":120, 
                "data": {
                    "txn_receiver": Constant.OFFLINE_TXN_RECEIVER.get(attrs["device"].country_code, attrs["mobile"])
                }
            }
        attrs["device"].send_new_otp(attrs["mobile"])
        return {"code":125, "data":{}}


class MobileWalletV2Serializer(serializers.Serializer):
    fcm_token = serializers.CharField()
    mobile = serializers.CharField()
    otp = serializers.CharField(required=False, max_length=6)
    is_wallet = serializers.BooleanField(required=False)
    is_exist = serializers.BooleanField(required=False)

    def validate(self, attrs):
        Validator.validate_mobile(attrs["mobile"])
        attrs["is_new"] = False
        FCM.validate(attrs["fcm_token"])
        device = Device.objects.get_by_mobile(attrs["mobile"])
        if not device:
            attrs["is_new"] = True
            return attrs
        # if device.is_wallet and device.fcm_token == attrs["fcm_token"]:        neccessary check removed for testing purpose only
        #     Responder.raise_error(118)
        if attrs.get("otp"):
            if not getattr(device, "otp"):
                Responder.raise_error(124)
            if Helper.is_time_over(device.otp_created_at, settings.OTP_EXPIRE_TIME):
                Responder.raise_error(122)
            if device.otp_verification_attempt >= settings.OTP_MAX_ATTEMPTS:
                # if not Helper.is_time_over(device.otp_created_at, settings.get("OTP_MAX_ATTEMPTS_TIMEOUT")):
                Responder.raise_error(184)
            if device.otp != attrs["otp"]:
                device.otp_verification_attempt = device.otp_verification_attempt + 1
                device.save()
                Responder.raise_error(123)
        elif device.otp_created_at and not Helper.is_time_over(device.otp_created_at, settings.OTP_RESEND_TIMEOUT):
            Responder.raise_error(126)
        attrs["device"] = device
        return attrs

    def create(self, attrs):
        is_new = attrs.pop("is_new")
        if is_new:
            country_code, mobile = attrs["mobile"].split("_", 1)
            attrs["device"] = Device.objects.create(
                country_code=country_code, fcm_token=attrs["fcm_token"], mobile=mobile
            )
        elif attrs.get("otp"):
            attrs["device"].confirm()
            return {"code": 120, "data": {}}

        if attrs.get("is_wallet"):
            attrs["device"].confirm_wallet(attrs["fcm_token"], attrs.get("is_exist"))
            payload = {
                "fcm_token": attrs["device"].fcm_token,
                "mobile": attrs["device"].mobile_number()
            }
            token = encode(payload, settings.SECRET_KEY, 'HS256')
            return {"code": 180, "data": {"token": token}}

        attrs["device"].send_new_otp(attrs["mobile"])

        if device := Device.objects.get_by_mobile_and_exclude_fcm_token(attrs["mobile"], attrs["fcm_token"]):
            if Account.objects.get_all_by_device_id(device_id=device.id):
                return {"code": 182, "data": {}}
        return {
            "code": 125,
            "data": {}
        }


class AccountCreationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'address',
            'device',
            'name',
            'is_imported',
            'is_primary'
        ]
        extra_kwargs = {
            'name': {'required': True},
            'is_imported': {'required': True}
        }
        model = Account

    def validate(self, attrs):
        attrs["device_id"] = self.context["device"].id
        attrs["account"] = Account.objects.get_by_device_and_address(attrs["device_id"], attrs["address"])

        if attrs["account"]:
            if attrs["account"].is_primary:
                return Responder.raise_error(191)
            if attrs.get("is_primary"):
                return attrs
            if attrs["account"].is_imported:
                Responder.raise_error(183)

        return attrs

    def create(self, attrs):
        Validator.validate_address(attrs['address'])
        if attrs.get("is_primary"):
            primary_accounts = Account.objects.get_primary_account(attrs["device_id"])
            primary_accounts.update(is_primary=False)
        if account := attrs.pop("account"):
            account.is_primary = attrs.get("is_primary", False)
            account.is_imported = attrs["is_imported"]
            account.name = attrs["name"]
            account.save()
            return account
        return Account.objects.create(**attrs)


class WalletAccountResetSerializer(serializers.Serializer):
    def create(self, attrs):
        kwargs = {"device_id": self.context["device"].id}
        if instance := Account.objects.filter(**kwargs):
            instance.update(is_deleted=True)
        self.context["device"].update({"fcm_token": None, "is_wallet": False, "is_verified": False})
        return {}


class ContactFromAddressSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)

    def validate(self, attrs):
        Validator.validate_address(attrs.get("address"))
        attrs["contacts"] = Contact.get_contacts_from_address(attrs.get("address"))
        return attrs
