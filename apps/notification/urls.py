from django.urls import path
from .views import (
    Notification, 
    NotificationAvailability,
)


urlpatterns = [
    path("", Notification.as_view()),
    path("/availability", NotificationAvailability.as_view()),
]