from django.urls import path

from .views import (
    GetAccountAssets,
    GetAlgorandAsset,
    DashboardView,
    GetAssetGraphView
)

urlpatterns = [
    path("", GetAlgorandAsset.as_view()),
    path("/dashboard", DashboardView.as_view()),
    path("/crpto-rate-graph", GetAssetGraphView.as_view()),
    path("/<str:address>", GetAccountAssets.as_view()),
]
