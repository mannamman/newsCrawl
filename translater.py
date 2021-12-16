# -*- coding: utf-8 -*-
import requests
import os
from threading import Thread

"""
papgo api 레퍼런스

ko	한국어
en	영어
ja	일본어
zh-CN	중국어 간체
zh-TW	중국어 번체
vi	베트남어
id	인도네시아어
th	태국어
de	독일어
ru	러시아어
es	스페인어
it	이탈리아어
fr	프랑스어

POST /v1/papago/n2mt HTTP/1.1
HOST: openapi.naver.com
User-Agent: curl/7.49.1
Accept: */*
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}
X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}
Content-Length: 51
"""

class Translater:
    def __init__(self, source_lang :str, target_lang :str, context_length :int, contexts :list, api :bool=False):
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
        if(api):
            self.cred = self.__load_cred()
        self.worker_num = context_length
        self.contexts = contexts
    
    def __load_cred(self):
        cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "cred/papagopasswd")
        with open(cred_path, "r") as f:
            cred = f.read()
            cred = cred.split(":")
        cred = [i.strip() for i in cred]
        return cred
    
    def __set_req_header(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": self.cred[0],
            "X-Naver-Client-Secret": self.cred[1]
        }
        return header


    def translate(self) -> list:
        """
        초기에 입력받은 데이터를 바탕으로 번역 진행
        번역은 api를 사용하므로 쓰레드를 이용하였음
        """
        threads = list()
        results = [0] * self.worker_num
        for i in range(self.worker_num):
            t = Thread(target=self.__translate, args=(i, results))
            threads.append(t)
        for thread in threads:
            thread.start()
        return results


    def __translate(self, idx :int, results :list):
        # api 사용
        # header = self.__set_req_header()
        # data = {
        #     "source" : self.source_lang,
        #     "target" : self.target_lang,
        #     "text" : self.contexts[idx]
        # }
        # res = requests.post(url=self.api_base_url, headers=header, data=data)
        # ## log 추가 필요, db 추가 필요
        # if(res.status_code == 200):
        #     result = res.json()
        #     result = result["message"]["result"]["translatedText"]
        #     # log(time, res.status_code)
        #     words = self.__context_strip(result)
        #     results[idx] = words
        # else:
        #     # log(time, res.text, res.status_code)
        #     pass

        # api 미사용
        words = self.__context_strip(self.contexts[idx])
        results[idx] = words

    def __context_strip(self, context :str) -> dict:
        context = context.replace("”", " ")
        context = context.replace("“", " ")
        context = context.replace(";", " ")
        words = context.split(" ")
        return words
