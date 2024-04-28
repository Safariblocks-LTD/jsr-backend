from rest_framework import serializers
from .models import Notification
from utils import Constant
from django.contrib.humanize.templatetags import humanize


class NotificationSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()
    
    def validate(self, attrs):
        attrs["net"] = getattr(Constant, f"{self.context['net_type'].upper()}_CODE")
        return attrs
    
    
class NotificationListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = ["id", "is_seen", "created_at", "data"]
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["created_at"] = humanize.naturaltime(instance.created_at)
        return response

