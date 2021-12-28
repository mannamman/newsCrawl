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

class UrlMaker:
    """
    언어에 맞는 뉴스의 url을 반환하는 클래스
    """
    def __init__(self, country :str):
        """
        입력받은 키워드를 바탕으로 구글에서 뉴스내용을 크롤링하는 클래스
        country : 특정 국가에서 검색한 내용을 얻기위한 국가 코드
        """
        self.country = country
        self.base_url = "https://www.google.com"
        self.crawl_timeout = 5


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


    def get_news_urls(self, keyword :str) -> list:
        """
        keyword를 입력받아서 뉴스 url을 반환
        """
        url = self.__make_search_new_url(keyword)
        html_text = requests.get(url, timeout=self.crawl_timeout).text
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


class Crawler:
    """
    크롤링만 하는 클래스
    """
    def __init__(self):
         self.CLEANR = re.compile('<.*?>')
         self.crawl_timeout = 5


    def __news_crawl(self, url :str) -> str:
        html_text = requests.get(url, timeout=self.crawl_timeout).text
        soup = BeautifulSoup(html_text, 'html.parser')
        p_classes = soup.find_all("p")
        context = ""
        try:
            for p_class in p_classes:
                context += p_class.get_text() + "\n"
                context = context.strip()
        except TypeError:
            pass
        except IndexError:
            pass
        return context


    def crawl(self, url):
        try:
            context = self.__news_crawl(url)
        except requests.exceptions.Timeout:
            # log?
            return ""
        cleantext = re.sub(self.CLEANR, ' ', context)
        cleantext = cleantext.strip().lower()
        return cleantext
    