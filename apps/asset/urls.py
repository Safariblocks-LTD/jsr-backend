from django.urls import path
from .views import (
    GetAssetOrOptInAssetOrCloseOutAsset, 
    GetMyAssetTransaction,
    TrendingTokenizableProducts,
    VerifyTitle,
    TopTokenizedAssets,
)


urlpatterns = [
    path("", GetAssetOrOptInAssetOrCloseOutAsset.as_view()),
    path("/<int:id>/transactions", GetMyAssetTransaction.as_view()),
    path('/trending-tokenizable-products', TrendingTokenizableProducts.as_view()),
    path('/update-title-status/<str:uuid>', VerifyTitle.as_view()),
    path('/top-tokenized-assets', TopTokenizedAssets.as_view()),
]
