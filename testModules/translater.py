# -*- coding: utf-8 -*-
import os
import six
# from google.cloud import translate
from google.cloud import translate_v3 as translate
## local 테스트 ##
from google.oauth2 import service_account
import asyncio


"""
구글 번역 api
공식 문서 : https://cloud.google.com/translate/docs/overview
공식 문서(개발문서) : https://googleapis.dev/python/translation/3.1.0/index.html
"""

# 상수
location = "us-central1"
project_id = os.getenv("project_id")

class Translater:
    def __init__(self):
        """
        Translater 클래스는 크롤링한 데이터를 받아 번역을 해주는 클래스
        """
        self.translate_client = self.__init_client()
        self.translate_timeout = 180
    
    def __init_client(self):
        global location
        global project_id
        ## local 테스트 ##
        cred_dir_path = os.path.dirname(os.path.abspath(__file__))
        cred_path = f"{cred_dir_path}/../cred/local_translate.json"
        credentials = service_account.Credentials.from_service_account_file(cred_path)
        translate_client = translate.TranslationServiceClient(credentials=credentials)
        self.parent = f"projects/{credentials.project_id}/locations/{location}"
        return translate_client

        ## 배포시 사용 ##
        translate_client = translate.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"
        return translate_client


    # def translate(self, context :str, source_lang :str, target_lang :str) -> list:
    #     results = list()
    #     # 불필요한 문자 제거
    #     context = self.__context_strip(context)
    #     # 문장 -> 단어들 변환
    #     words = self.__word_preprocess(context)
    #     # api 사용
    #     res = self.translate_client.translate_text(
    #         parent=self.parent,
    #         contents=words,
    #         mime_type="text/plain",
    #         source_language_code=source_lang,
    #         target_language_code=target_lang,
    #         timeout = self.translate_timeout
    #     )
    #     results = [word.translated_text for word in res.translations]
    #     return results


    def batch_translate(self, source_lang :str, target_lang :str, input_uri :str, output_uri :str) -> list:
        gcs_source = {"input_uri": input_uri}

        input_configs_element = {
            "gcs_source": gcs_source,
            "mime_type": "text/plain",  # Can be "text/plain" or "text/html".
        }
        
        gcs_destination = {"output_uri_prefix": output_uri}
        output_config = {"gcs_destination": gcs_destination}
        # Supported language codes: https://cloud.google.com/translate/docs/languages
        operation = self.translate_client.batch_translate_text(
            request={
                "parent": self.parent,
                "source_language_code": source_lang,
                "target_language_codes": [target_lang],  # Up to 10 language codes here.
                "input_configs": [input_configs_element],
                "output_config": output_config,
            }
        )
        response = operation.result(self.translate_timeout)

        print("Total Characters: {}".format(response.total_characters))
        print("Translated Characters: {}".format(response.translated_characters))

        
if(__name__ == "__main__"):
    t = Translater()
    input_uri = "gs://crawl-bucket/input/7af4c2e7-a04a-41fb-832c-66b9cbba4c69.txt/"
    output_uri = "gs://crawl-bucket/output/7af4c2e7-a04a-41fb-832c-66b9cbba4c69.txt/"
    t.batch_translate("en", "ko", input_uri, output_uri)