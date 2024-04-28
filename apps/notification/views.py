from rest_framework.views import APIView
from utils import Responder
from .models import Notification as NotificationModel
from .serializers import (
    NotificationSerializer, 
    NotificationListSerializer
)
from jasiri_wallet.permissions import Public


class Notification(APIView):
    permission_classes = [Public]
    
    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data, context={"net_type":kwargs["net_type"]})
        serializer.is_valid(raise_exception=True)
        notifications = NotificationModel.objects.get_all(**serializer.validated_data)
        notifications_ = NotificationListSerializer(notifications, many=True).data
        NotificationModel.objects.update_seen()
        return Responder.send(135 if len(notifications_) else 136, notifications_)
    

class NotificationAvailability(APIView):
    permission_classes = [Public]
        
    def post(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data, context={"net_type":kwargs["net_type"]})
        serializer.is_valid(raise_exception=True)
        availability = NotificationModel.objects.get_availability(**serializer.validated_data)
        return Responder.send(137, {"available": availability})
    
