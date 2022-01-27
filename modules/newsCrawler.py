# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from testModules.translater import Translater
import os
import re
import copy

"""
현재까지 알아낸 국가코드 (google)

eng : https://news.google.com/topstories?hl=en
fr : https://news.google.com/topstories?hl=fr
jp : https://news.google.com/topstories?hl=ja
kr : https://news.google.com/topstories?hl=kr


예시
eng : https://news.google.com/search?q=snp500&hl=en-US&gl=US

뉴스 url이 저장된 클래스 id
h3 = ipQwMb ekueJc RD0gLb

"""
# g-card class="ftSUBd"

# https://dojang.io/mod/page/view.php?id=2469 async 참고 자료

translater = Translater()


class HeaderCrawler:
    """
    언어에 맞는 뉴스의 url을 반환하는 클래스
    """
    def __init__(self, country :str):
        """
        입력받은 키워드를 바탕으로 구글에서 뉴스내용을 크롤링하는 클래스
        country : 특정 국가에서 검색한 내용을 얻기위한 국가 코드
        """
        self.country = country
        self.base_url = "https://news.google.com"
        self.crawl_timeout = 5


    def __make_search_new_url(self, keyword :str):
        # return f"{self.base_url}/search?q={keyword}&hl={self.country}&tbm=nws&lr=lang_{self.country}"
        return f"{self.base_url}/search?q={keyword}&hl={self.country}&gl=en"


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


    def get_news_header(self, keyword :str) -> list:
        url = self.__make_search_new_url(keyword)
        print(url)
        html_text = requests.get(url, timeout=self.crawl_timeout).text
        soup = BeautifulSoup(html_text, 'html.parser')
        news_cards_list = soup.find_all("h3", "ipQwMb ekueJc RD0gLb")
        news_headers = []
        for news_card in news_cards_list:
            news_headers.append(news_card.text)
        translated_header = None
        if(self.country != "en"):
            translated_header = copy.copy(news_headers)
            translated_header = self._to_eng(translated_header)
        return news_headers ,translated_header


    def _to_eng(self, headers):
        global translater
        en_headers = translater.translate(headers, self.country, "en")
        return en_headers

if(__name__ == "__main__"):
    news_header = HeaderCrawler("en")
    print(news_header.get_news_header("tesla"))
