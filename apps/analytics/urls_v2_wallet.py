from django.urls import path
from .views import (
    ProtocolAnalyticView
)


urlpatterns = [
    path("/protocol-analytic", ProtocolAnalyticView.as_view())
]