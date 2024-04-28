from rest_framework import serializers
from .models import Feedback, LocationAddress


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class LocationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationAddress
        fields = '__all__'