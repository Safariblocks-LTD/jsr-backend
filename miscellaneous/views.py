from rest_framework.views import APIView
from jasiri_wallet.permissions import Public
from utils import Responder, Helper, NewsScrapper, Constant

class News(APIView):
    permission_classes = [Public]

    def get(self, request, **kwargs):
        lang = request.GET.get('lang')
        lang = 'en' if not lang else lang
        cache_key = 'LATEST_MARKET_NEWS'
        news = Helper.getCachedData(cache_key)
        topics = Constant.NewsTopic.choices()
        if not news:
            news_list = []
            for topic in topics:
                news = NewsScrapper.getNews(topic[1], lang)[0]
                news_list.append(news)
                Helper.setCacheData(cache_key, news_list)
            return Responder.send(139, news_list)
        return Responder.send(139, news)
    
    def post(self, request, **kwargs):
        cache_key = 'LATEST_MARKET_NEWS'
        Helper.deleteCacheData(cache_key)
        return Responder.send(166)