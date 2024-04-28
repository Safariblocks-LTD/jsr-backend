from django.urls import path
from .views import (
    Transaction, 
    TwilioTransaction,
    AfricasTalkingTransaction,
)


urlpatterns = [
    path("", Transaction.as_view()),
    path("/offline-handler/twilio", TwilioTransaction.as_view()),
    path("/offline-handler/africastalking", AfricasTalkingTransaction.as_view()),
]