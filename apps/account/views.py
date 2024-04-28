from rest_framework.views import APIView
from jasiri_wallet.permissions import WriteOnly, Public
from utils import (
    Responder, 
    Algorand,
)
from .serializers import (
    AccountDetailSerializer, 
    AccountRegistrationSerializer, 
    AccountRemoveSerializer, 
    AccountMobileSerializer,
    JWTAccountRegistrationSerializer,
    MobileWalletV2Serializer,
    AccountCreationSerializer,
    WalletAccountResetSerializer,
    ContactFromAddressSerializer
)
from .models import Account as AccountModel
from utils.contact import Contact
from jasiri_wallet.authentication import PublicAuthentication


class AccountV2(APIView):
    authentication_classes = [PublicAuthentication]
    permission_classes = (Public,)

    def post(self, request, **kwargs):
        serializer = JWTAccountRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Responder.send(112, data)

class Account(APIView):
    permission_classes = (WriteOnly,)
    
    def get(self, request, **kwargs):
        details = Algorand.get_account_info(request.user.address)
        details = AccountDetailSerializer(details).data
        return Responder.send(105, details)
    
    def post(self, request, **kwargs):
        serializer = AccountRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Responder.send(112, data)
        
        
class AccountLogout(APIView):
    
    def post(self, request, **kwargs):
        serializer = AccountRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(address=request.user.address)
        return Responder.send(114)
    

class AccountReset(APIView):

    def post(self, request, **kwargs):
        serializer = AccountRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(115)


class AccountMobile(APIView):

    def post(self, request, **kwargs):
        serializer = AccountMobileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Responder.send(**serializer.save())


class MobileWalletV2View(APIView):
    authentication_classes = [PublicAuthentication]
    permission_classes = (Public,)

    def post(self, request, **kwargs):
        serializer = MobileWalletV2Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Responder.send(**serializer.save())


class WalletAccountView(APIView):
    permission_classes = (Public,)

    def get(self, request, **kwargs):
        queryset = AccountModel.objects.get_all_by_device_id(request.user.id)
        serializer = AccountCreationSerializer(
            queryset, many=True
        )
        return Responder.send(105, serializer.data)

    def post(self, request, **kwargs):
        serializer = AccountCreationSerializer(data=request.data, context={"device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(112, serializer.data)


class WalletAccountResetView(APIView):
    permission_classes = (Public,)

    def post(self, request, **kwargs):
        serializer = WalletAccountResetSerializer(data=request.data, context={"device": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(115)


class WalletContactsWithAddressView(APIView):
    permission_classes = (Public,)

    def post(self, request, **kwargs):
        data = Contact.get_contacts_with_address(request.data["contacts"])
        return Responder.send(192, data)


class GetContactFromAddressView(APIView):
    permission_classes = (Public,)

    def post(self, request, **kwargs):
        serializer = ContactFromAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if not data["contacts"]:
            return Responder.send(202)
        data = data["contacts"][0]
        return Responder.send(201, data)
