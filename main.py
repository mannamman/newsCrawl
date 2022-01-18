from modules.newsCrawler import Crawler, UrlMaker
from modules.translater import Translater
from modules.mongo_db import DBworker
from threading import Thread
from flask import Flask, request
import json
import functools
from modules.req_valid import auth_deco
# log
from google.cloud import logging_v2
from google.cloud.logging_v2 import Resource
import traceback


app = Flask(__name__)
logging_client = logging_v2.Client()
resource = Resource(type="cloud_function", labels={"function_name":"news-crawl", "region":"asia-northeast3"})
logger = logging_v2.Logger(name="news-crawl",client=logging_client , resource=resource)
# 객체 초기화(공통으로 사용되는)
crawler = Crawler()
translater = Translater()

# 디버그 로그 작성
def debug_log(msg :str):
    global logger
    logger.log_text(msg, severity="DEBUG")


def error_log(msg :str):
    global logger
    logger.log_text(f"ERROR LOG : {msg}", severity="ERROR")


def abstract_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(request)
    return wrapper


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


def run(
    url :str, crawler :Crawler, translater :Translater, idx :int,
    context_results :list, source_lang :str, target_lang :str
):
    print(f"thread {idx} start")
    context = crawler.crawl(url)
    if(context == ""):
        print(f"thread {idx} fail")
        context_results[idx] = ""
        return
    result = translater.translate(context, source_lang, target_lang)
    context_results[idx] = result
    print(f"thread {idx} done")


@app.route("/ping", methods=["GET"])
@abstract_request
@auth_deco
def ping_pong(req):
    return("pong", 200)


@app.route("/crawl", methods=["POST"])
@abstract_request
@auth_deco
def crawl(req):
    global crawler
    global translater
    try:
        # post 메시지 파싱
        recevied_msg = json.loads(req.get_data().decode("utf-8"))
        subject = recevied_msg["subject"]
        source_lang = recevied_msg["source_lang"]
        target_lang = recevied_msg["target_lang"]

        # get urls
        url_maker = UrlMaker(source_lang)
        urls = url_maker.get_news_urls(subject)

        # db worker 객체 생성
        db_worker = DBworker(database=subject, collection=target_lang)

        # 쓰레드 실행
        threads = list()
        context_results = [0] * len(urls) # 결과 값을 받기위한 배열

        for idx, url in enumerate(urls):
            thread = Thread(target=run, args=(url, crawler, translater, idx, context_results, source_lang, target_lang))
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
        db_worker.save_error(context_results)
        return(error, 400)


if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=8080, debug=False)