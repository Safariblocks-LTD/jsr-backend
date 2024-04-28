from django.urls import path
from .views import *


urlpatterns = [
    path('/protocol-feed', ProtocolTransactionView.as_view()),
]