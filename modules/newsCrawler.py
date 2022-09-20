# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from modules.translator import Translator
import copy
from typing import List, Tuple
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

translator = Translator()


class HeaderCrawler:
    """
    언어에 맞는 뉴스의 url을 반환하는 클래스
    """
    def __init__(self, country: str) -> None:
        """
        입력받은 키워드를 바탕으로 구글에서 뉴스내용을 크롤링하는 클래스
        country : 특정 국가에서 검색한 내용을 얻기위한 국가 코드
        """
        self.country = country
        self.base_url = "https://news.google.com"
        self.crawl_timeout = 5


    def __make_search_new_url(self, keyword: str) -> str:
        # return f"{self.base_url}/search?q={keyword}&hl={self.country}&tbm=nws&lr=lang_{self.country}"
        return f"{self.base_url}/search?q={keyword}&hl={self.country}&gl=en"


    def __make_news_link(self, url: str, href: str) -> str:
        base_url = "/".join(url.split("/")[:3])
        href = href[1:]
        news_link = base_url + href
        return news_link      


    def get_news_header(self, keyword: str) -> Tuple[List[str], List[str], List[str]]:
        url = self.__make_search_new_url(keyword)
        html_text = requests.get(url, timeout=self.crawl_timeout).text
        soup = BeautifulSoup(html_text, 'html.parser')
        news_cards_list = soup.find_all("h3", "ipQwMb ekueJc RD0gLb")
        news_headers = []
        news_links = []
        for news_card in news_cards_list:
            a_tag = news_card.find("a", href=True)
            a_href = a_tag["href"]
            news_link = self.__make_news_link(url, a_href)
            news_links.append(news_link)
            news_headers.append(news_card.text)
        translated_header = None
        if(self.country != "en"):
            translated_header = copy.copy(news_headers)
            translated_header = self._to_eng(translated_header)
        return news_headers ,translated_header, news_links


    def _to_eng(self, headers: List[str]) -> List[str]:
        global translator
        en_headers = translator.translate(headers, self.country, "en")
        return en_headers

# test code
if(__name__ == "__main__"):
    news_header = HeaderCrawler("en")
    news_header.get_news_header("tesla")
