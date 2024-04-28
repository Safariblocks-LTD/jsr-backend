from django.urls import path

from .views import (
    MobileWalletV2View,
    WalletAccountView,
    WalletAccountResetView,
    WalletContactsWithAddressView,
    GetContactFromAddressView
)

urlpatterns = [
    path("/create-wallet", MobileWalletV2View.as_view()),
    path("", WalletAccountView.as_view()),
    path("/reset", WalletAccountResetView.as_view()),
    path("/contacts-to-address", WalletContactsWithAddressView.as_view()),
    path("/contact-from-address", GetContactFromAddressView.as_view()),
]
