from django.urls import path
from .views import (
    Analytics,
    TopTokenizedAssetsView,
    TokenizedAssetChart,
    ProtocolAnalyticView
)


urlpatterns = [
    path("", Analytics.as_view()),
    path("/top", TopTokenizedAssetsView.as_view()),
    path("/chart", TokenizedAssetChart.as_view()),
]