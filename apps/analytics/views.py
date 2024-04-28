from rest_framework.views import APIView
from utils import (
    Responder, 
    Dynamodb,
)
from .models import Brand, ChartDataSet, TopTokenizedAsset
from .serializers import BrandSerializer, ChartSerializer, ProtocolAnalyticSerializer
from utils.helpers import Helper
from jasiri_wallet.permissions import Public
from django.core.cache import cache


class Analytics(APIView):
    def get(self, request, *args, **kwargs):
        return Responder.send(138, Dynamodb.get_analytics(kwargs["net_type"]))
    


class TopTokenizedAssetsView(APIView):
    permission_classes = [Public]
    def get(self, request, *args, **kwargs):
        cache_key = 'TOP_TOKENIZED_ASSETS'
        data = Helper.getCachedData(cache_key)
        if data:
            return Responder.send(138, data)
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        Helper.setCacheData(cache_key, serializer.data)
        return Responder.send(138, serializer.data)
    

class TokenizedAssetChart(APIView):
    permission_classes = [Public]
    def get(self, request, *args, **kwargs):
        dataset = ChartDataSet.objects.get_chart_data_by_ticker(request.GET.get('ticker_name'))
        serializer = ChartSerializer(dataset, many=True)
        return Responder.send(138, serializer.data)


class ProtocolAnalyticView(APIView):
    permission_classes = [Public]

    def get(self, request, **kwargs):
        if not (data := cache.get(f"{kwargs['net_type']}_protocol_analytic")):
            serializer = ProtocolAnalyticSerializer(request.data, context={"net_type": kwargs["net_type"]})
            data = serializer.data
            cache.set(f"{kwargs['net_type']}_protocol_analytic", data, 6*60*60)
        return Responder.send(138, data)
