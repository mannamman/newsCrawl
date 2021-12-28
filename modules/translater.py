# -*- coding: utf-8 -*-
import os
import six
from google.cloud import translate_v3 as translate
## local 테스트 ##
# from google.oauth2 import service_account

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

"""
구글 번역 api
공식 문서 : https://cloud.google.com/translate/docs/overview
공식 문서(개발문서) : https://googleapis.dev/python/translation/3.1.0/index.html
"""

# 상수
location = "global"
project_id = os.getenv("project_id")

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
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api = api
        self.max_size = 1024
        self.stops = set(stopwords.words('english'))
        if(api):
            self.translate_client = self.__init_client()
    
    def __init_client(self):
        global location
        global project_id
        ## local 테스트 ##
        # cred_path = f"{os.getcwd()}/cred/local_translate.json"
        # credentials = service_account.Credentials.from_service_account_file(cred_path)
        # translate_client = translate.TranslationServiceClient(credentials=credentials)
        # self.parent = f"projects/{credentials.project_id}/locations/{location}"
        # return translate_client

        ## 배포시 사용 ##
        translate_client = translate.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"
        return translate_client


    def __word_preprocess(self, context :str) -> list:
        # 불필요한 수식 제거
        context = self.__context_strip(context)
        # 불용어 제거
        word_tokens = word_tokenize(context)
        result = []
        for word in word_tokens:
            if word not in self.stops:
                result.append(word)
        return result


    def translate(self, context :str) -> list:
        results = list()
        # 불필요한 문자 제거
        context = self.__context_strip(context)
        # 문장 -> 단어들 변환
        words = self.__word_preprocess(context)
        if(self.api):
            # api 사용
            res = self.translate_client.translate_text(
                parent=self.parent,
                contents=words,
                mime_type="text/plain",
                source_language_code=self.source_lang,
                target_language_code=self.target_lang
            )
            results = [word.translated_text for word in res.translations]
        else:
            # api 미사용
            pass
        return results
        

    def __context_strip(self, context :str) -> str:
        context = context.replace("”", "")
        context = context.replace("“", "")
        context = context.replace(";", "")
        # words = context.split(" ")
        return context