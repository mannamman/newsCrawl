from newsCrawler import Crawler, UrlMaker
from translater import Translater
from mongo_db import DBworker
from threading import Thread
from flask import Flask, request
import json
# log
from google.cloud import logging_v2
from google.cloud.logging_v2 import Resource
import traceback

app = Flask(__name__)
logging_client = logging_v2.Client()
resource = Resource(type="cloud_function", labels={"function_name":"news-crawl", "region":"asia-northeast3"})
logger = logging_v2.Logger(name="news-crawl",client=logging_client , resource=resource)

# 디버그 로그 작성
def debug_log(msg :str):
    global logger
    logger.log_text(msg, severity="DEBUG")


def error_log(msg :str):
    global logger
    logger.log_text(f"ERROR LOG : {msg}", severity="ERROR")


def pretty_trackback(msg :str)->str:
    """
    에러 발생시 문구를 보기 편하게 변환하는 함수
    파라미터
        msg : traceback 모듈을 이용해 전달받은 에러 메시지
    반환 값
        변환된 에러 메시지
    """
    msg = msg.split("\n")
    msg = msg[1:-1]
    msg = [i.strip() for i in msg]
    msg = " ".join(msg)
    return msg


def run(url :str, crawler :Crawler, translater :Translater, idx :int, context_results :list):
    print(f"thread {idx} start")
    context = crawler.crawl(url)
    if(context == ""):
        print(f"thread {idx} fail")
        context_results[idx] = ""
        return
    result = translater.translate(context)
    context_results[idx] = result
    print(f"thread {idx} done")


@app.route("/ping", methods=["GET"])
def ping_pong():
    return("pong", 200)


@app.route("/crawl", methods=["POST"])
def crawl():
    try:
        # post 메시지 파싱
        recevied_msg = json.loads(request.get_data().decode("utf-8"))
        subject = recevied_msg["subject"]
        source_lang = recevied_msg["source_lang"]
        target_lang = recevied_msg["target_lang"]
        api = recevied_msg["api"]

        # get urls
        url_maker = UrlMaker(source_lang)
        urls = url_maker.get_news_urls(subject)

        # 객체 초기화
        crawler = Crawler()
        translater = Translater(source_lang=source_lang, target_lang=target_lang, api=api)
        db_worker = DBworker(database=subject, collection=target_lang)

        # 쓰레드 실행
        threads = list()
        context_results = [0] * len(urls) # 결과 값을 받기위한 배열

        for idx, url in enumerate(urls):
            thread = Thread(target=run, args=(url, crawler, translater, idx, context_results))
            threads.append(thread)
        for thread in threads:
            thread.start()

        # 남은 쓰레드 대기
        while True:
            if(0 not in context_results):
                break
        db_worker.save_result(context_results)
        return("ok", 200)
    except Exception:
        error = traceback.format_exc()
        error = pretty_trackback(error)
        error_log(error)
        return(error, 400)


if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=8080, debug=False)