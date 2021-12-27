# -*- coding: utf-8 -*-
import os
import six
from google.cloud import translate_v2 as translate

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

"""
구글 번역 api
공식 문서 : https://cloud.google.com/translate/docs/overview
공식 문서(개발문서) : https://googleapis.dev/python/translation/3.1.0/index.html
"""

class Translater:
    def __init__(self, source_lang :str, target_lang :str, api :bool=False):
        """
        Translater 클래스는 크롤링한 데이터를 받아 번역을 해주는 클래스
        source_lang : 크롤링한 원본 언어
        target_lang : 결과 언어
        context_length : 크롤링한 페이지의 개수
        contexts : 페이지의 내용들
        """
        self.api_base_url = "https://openapi.naver.com/v1/papago/n2mt"
        self.http_method = "POST"
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api = api
        if(api):
            self.translate_client = self.__init_client()

    
    def __init_client(self):
        # cred_path = f"{os.getcwd()}/cred/local_translate.json"
        # credentials = service_account.Credentials.from_service_account_file(cred_path)
        # translate_client = translate.Client(credentials=credentials)
        translate_client = translate.Client()
        return translate_client


    def __word_preprocess(self, context :str) -> list:
        # 불필요한 수식 제거
        context = self.__context_strip(context)
        # 불용어 제거
        word_tokens = word_tokenize(context)
        stops = set(stopwords.words('english'))
        result = []
        for word in word_tokens:
            if word not in stops:
                result.append(word)
        # return_str = " ".join(result)
        return result


    def translate(self, context :str) -> list:
        results = list()
        words = self.__word_preprocess(context)
        if(self.api):
            # api 사용
            for word in words:    
                if isinstance(word, six.binary_type):
                    word = word.decode("utf-8")
                trans_result = self.translate_client.translate(word, target_language=self.target_lang)["translatedText"]
                results.append(trans_result)
                # words = self.__context_strip(trans_result)
            
        else:
            # api 미사용
            # words = self.__context_strip(context)
            pass
        return results
        

    def __context_strip(self, context :str) -> str:
        context = context.replace("”", "")
        context = context.replace("“", "")
        context = context.replace(";", "")
        # words = context.split(" ")
        return context