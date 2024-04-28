from rest_framework.views import APIView
from .serializers import FeedbackSerializer, LocationAddressSerializer
from utils.responder import Responder
from .models import LocationAddress
from jasiri_wallet.permissions import Public


class FeedbackView(APIView):
    permission_classes = [Public]
    
    def post(self, request, **kwargs):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Responder.send(167)
        return Responder.raise_error(168)
 

class LocationAddressView(APIView):
    permission_classes = [Public]

    def get(self, request, **kwargs):
        search = request.GET.get('search')
        locations = LocationAddress.objects.get_all_addresses_by_search(search)
        serializers = LocationAddressSerializer(locations, many=True)
        return Responder.send(169 if len(locations) else 170, serializers.data)