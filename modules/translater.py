# -*- coding: utf-8 -*-
import os
from typing import List, Dict, Tuple
# from google.cloud import translate
from google.cloud import translate_v3 as translate



"""
구글 번역 api
공식 문서 : https://cloud.google.com/translate/docs/overview
공식 문서(개발문서) : https://googleapis.dev/python/translation/3.1.0/index.html
"""

# 상수
location = "global"
project_id = os.getenv("project_id")

class Translater:
    def __init__(self) -> None:
        """
        Translater 클래스는 크롤링한 데이터를 받아 번역을 해주는 클래스
        """
        self.translate_client = self.__init_client()
        self.translate_timeout = 180
    
    def __init_client(self):
        global location
        global project_id

        ## 배포시 사용 ##
        translate_client = translate.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"
        return translate_client


    def translate(self, headers: str, source_lang: str, target_lang: str="en") -> List[str]:
        results = list()
        # api 사용
        res = self.translate_client.translate_text(
            parent=self.parent,
            contents=headers,
            mime_type="text/plain",
            source_language_code=source_lang,
            target_language_code=target_lang,
            timeout = self.translate_timeout
        )
        results = [word.translated_text for word in res.translations]
        return results


    def get_supported_lang(self) -> None:
        res = self.translate_client.get_supported_languages(parent=self.parent)
        # List language codes of supported languages.
        print("Supported Languages:")
        for language in res.languages:
            print("Language Code: {}".format(language.language_code))


    def batch_translate(
            self,
            source_lang :str,
            target_lang :str,
            input_uri :str,
            output_uri :str,
            subject :str
        ) -> None:
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

        total_char = response.total_characters
        translated_char = response.translated_characters
        log_msg = f"{subject=}, {source_lang=}, {target_lang=}, {total_char=}, {translated_char=}, {input_uri=}, {output_uri=}"

        
if(__name__ == "__main__"):
    t = Translater()