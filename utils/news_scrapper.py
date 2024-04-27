from .helpers import Helper

class NewsScrapper:

    @classmethod
    def getNews(cls, topic, lang):
        url = f"https://news.google.com/search?q={topic}&hl={lang}"
        soup = Helper.getSoup(url)
        news = cls.__getNews(soup)
        news[0]['article']['description'] = cls.__getFirstNewsDescription(topic, lang)
        return news

    @classmethod
    def __getNews(cls, soup):
        items = soup.find_all("c-wiz", {"class" : "PO9Zff Ccj79 kUVvS"})
        news = [cls.__getJSON(item) for item in items[0:1]]
        return news
    
    @classmethod
    def __getJSON(cls, item):
        return {
            'article':{
                'title': cls.__getArticleTitle(item),
                'image': cls.__getArticleImage(item),
                'link' : cls.__getArticleLink(item),
            },
            'source':{
                'name': cls.__getSourceName(item),
            }
        }
    
    @staticmethod
    def __getArticleTitle(item):
        return item.find("a", {"class": "JtKRv"}).getText()

    
    @staticmethod
    def __getArticleImage(item):
        try:
            return "https://news.google.com" + item.find("img", {"class" : "Quavad"}).get("src").replace('w200-h112', 'w500-h320')
        except:
            return None
    
    @staticmethod
    def __getArticleLink(item):
        articleLink = item.find("a", {"class": "WwrzSb"}).get("href")
        return "https://news.google.com"+articleLink[1:]
    
    @staticmethod
    def __getSourceName(item):
        return item.find("div", {"class" : "vr1PYe"}).getText()
    
    # @staticmethod
    # def __getSourceImage(item):
    #     return item.find("img", {"class" : "msvBD zC7z7b"}).get("src")
    
    @staticmethod
    def __getFirstNewsDescription(topic, lang):
        url = f"https://www.google.com/search?q={topic}&tbm=nws&hl={lang}"
        soup = Helper.getSoup(url)
        items = soup.find_all("div", {"class" : "SoaBEf"})
        descr = items[0].find('div', {'class':'GI74Re nDgy9d'}).getText()
        return descr
    
    
    






