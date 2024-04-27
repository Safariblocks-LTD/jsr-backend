from rest_framework.authentication import BaseAuthentication
from utils import AlgorandUser, Responder, Helper
from django.conf import settings
from apps.account.models import Account, Device

class PublicAuthentication(BaseAuthentication):

    def authenticate(self, request):
        return (True, None)
    
    
class UserTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        if request.path.startswith("/v2/wallet/"):
            return self.walletAuthentication(request)
        if request.path.startswith("/v2"):
            return self.jwtAuthentication(request)
        private_key = request.headers.get("X-Algorand-Key")
        user = AlgorandUser(private_key) if private_key else None
        return (user, None)

    def walletAuthentication(self, request):
        access_token = request.headers.get("Authorization")
        if not access_token:
            Responder.raise_error(514)
        payload = Helper.jwt_decode(access_token)
        device = Device.objects.get_by_fcm_and_mobile(
            payload.get('fcm_token'), payload.get('mobile')
        )
        if device and getattr(device, "is_wallet"):
            return (device, None)
        else:
            Responder.raise_error(117)

    def jwtAuthentication(self, request):
        access_token = request.headers.get("Authorization")
        if not access_token:
            Responder.raise_error(514)
        payload = Helper.jwt_decode(access_token)
        if account := Account.objects.get_account_by_id(payload.get('account_id')):
            return (account, None)
        else:
            Responder.raise_error(117)
