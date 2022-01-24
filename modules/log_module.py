# log
from google.cloud import logging_v2
from google.cloud.logging_v2 import Resource

class Logger:
    def __init__(self):
        logging_client = logging_v2.Client()
        resource = Resource(type="cloud_function", labels={"function_name":"news-crawl", "region":"asia-northeast3"})
        self.logger = logging_v2.Logger(name="news-crawl",client=logging_client , resource=resource)


    # 디버그 로그 작성
    def debug_log(self, msg :str):
        self.logger.log_text(msg, severity="DEBUG")


    def error_log(self, msg :str):
        self.logger.log_text(f"ERROR LOG : {msg}", severity="ERROR")


    def info_log(self, msg :str):
        self.logger.log_text(f"INFO : {msg}", severity="INFO")