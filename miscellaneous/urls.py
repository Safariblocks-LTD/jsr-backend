from django.urls import path
from .views import *


urlpatterns = [
    path('/latest_market_news', News.as_view()),
]
