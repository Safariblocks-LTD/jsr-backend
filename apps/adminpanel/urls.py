from django.urls import path
from .views import FeedbackView, LocationAddressView

urlpatterns = [
    path("/feedback", FeedbackView.as_view()),
    path("/locations", LocationAddressView.as_view())
]