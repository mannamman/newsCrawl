# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import re

"""
현재까지 알아낸 국가코드 (google)

eng : https://www.google.co.uk/webhp?hl=en
fr : https://www.google.fr/webhp?hl=fr
jp : https://www.google.com/webhp?hl=ja
kr : https://www.google.com/webhp?hl=kr

예시
https://www.google.com/search?q=stackoverflow&hl=ja

뉴스 url이 저장된 클래스 id
div id = ZINbbc xpd O9g5cc uUPGi

"""
# g-card class="ftSUBd"
timeout = 5

class Crawler:
    def __init__(self, country :str):
        """
        입력받은 키워드를 바탕으로 구글에서 뉴스내용을 크롤링하는 클래스
        country : 특정 국가에서 검색한 내용을 얻기위한 국가 코드
        """
        self.country = country
        self.base_url = "https://www.google.com"
        # self.CLEANR = re.compile('[^a-zA-Z]')
        self.CLEANR = re.compile('<.*?>') 
    
    def __make_search_new_url(self, keyword :str):
        return f"{self.base_url}/search?q={keyword}&hl={self.country}&tbm=nws"
    
    def __check_cache(self, urls):
        if(os.path.exists("cache")):
            with open("cache", "r") as f:
                cache_list = f.read()
            with open("cache", "w") as f:
                f.write("\n".join(urls))
            cache_list = cache_list.split("\n")
            for cache_url in cache_list:
                if(cache_url in urls):
                    print("cache!", cache_url)
                    urls.remove(cache_url)
        else:
            with open("cache", "w") as f:
                f.write("\n".join(urls))
        return urls

    def __get_news_urls(self, url :str) -> list:
        print("get news url...")
        html_text = requests.get(url, timeout=timeout).text
        soup = BeautifulSoup(html_text, 'html.parser')
        news_cards_list = soup.find_all(class_="ZINbbc xpd O9g5cc uUPGi")
        news_urls = []
        for news_card in news_cards_list:
            # print(news_card)
            a = news_card.find("a")
            href = a["href"]
            if("https" in href):
                url_index = href.index("https")
            elif("http" in href):
                url_index = href.index("http")
            else:
                continue
            url = href[url_index:]
            param_index = url.index("&")
            url = url[:param_index]
            news_urls.append(url)
        return news_urls

    def __news_crawl(self, url :str) -> str:
        print(f"{url} crawl start")
        html_text = requests.get(url, timeout=timeout).text
        soup = BeautifulSoup(html_text, 'html.parser')
        p_classes = soup.find_all("p")
        context = ""
        try:
            for p_class in p_classes:
                context += str(p_class.contents[0]) + "\n"
                context = context.strip()
        except TypeError:
            pass
        except IndexError:
            pass
        return context


    # def __word_preprocess(self, context :str) ->str:
    #     import nltk
    #     try:
    #         from nltk.corpus import stopwords
    #     except ModuleNotFoundError:
    #         nltk.download()
    #     print("start word process")
    #     # 불용어 제거
    #     stops = set(stopwords.words('english'))
    #     no_stops = [word for word in context if not word in stops]
    #     stemmer = nltk.stem.SnowballStemmer('english')
    #     stemmer_words = [stemmer.stem(word) for word in no_stops]
    #     return(" ".join(stemmer_words))


    def crawl(self, keyword :str):
        url = self.__make_search_new_url(keyword)
        news_urls = self.__get_news_urls(url)
        # news_urls = self.__check_cache(news_urls)
        contexts = []
        for news_url in news_urls:
            try:
                context = self.__news_crawl(news_url)
            except requests.exceptions.Timeout:
                print(f"{news_url} time out!!")
                continue
            cleantext = re.sub(self.CLEANR, ' ', context)
            cleantext = cleantext.strip().lower().split()
            # processed_test = self.__word_preprocess(cleantext)
            # contexts.append(processed_test)
            contexts.append(" ".join(cleantext))
        return contexts

    