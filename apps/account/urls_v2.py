from django.urls import path, re_path

from .views import (
    AccountV2,
)

urlpatterns = [
    path("", AccountV2.as_view()),
]