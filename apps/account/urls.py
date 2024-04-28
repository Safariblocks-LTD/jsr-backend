from django.urls import path
from .views import (
    Account, 
    AccountLogout, 
    AccountReset,
    AccountMobile,
)


urlpatterns = [
    path("", Account.as_view()),
    path("/logout", AccountLogout.as_view()),
    path("/reset", AccountReset.as_view()),
    path("/mobile", AccountMobile.as_view()),
]