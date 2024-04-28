from django.urls import path

from .views import (
    TransactionV2WalletView,
    ExportTransactionHistoryV2WalletView,
    RequestTransactionWalletV2View,
    UpdateRequestTransactionWalletV2View
)

urlpatterns = [
    path("/request", RequestTransactionWalletV2View.as_view()),
    path("/request/<int:pk>", UpdateRequestTransactionWalletV2View.as_view()),
    path("/<str:address>", TransactionV2WalletView.as_view()),
    path("/<str:address>/csv", ExportTransactionHistoryV2WalletView.as_view()),
]
