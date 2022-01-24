## moduels ##
from modules.newsCrawler import HeaderCrawler
from modules.mongo_db import DBworker
from modules.file_worker import FileWorker
from modules.req_valid import auth_deco
from modules.log_module import Logger

## sentiment sentiment analysis
from sentiment_dir.sentiment import NewsSentiment

# web server
from flask import Flask, request

# bulit in
import json
import functools
import traceback
import pytz
import datetime



app = Flask(__name__)

logger = Logger()

# 객체 초기화(공통으로 사용되는)
target_lang ="en"
file_worker = FileWorker()
news_sentiment = NewsSentiment()
KST = pytz.timezone("Asia/Seoul")


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



@app.route("/ping", methods=["GET"])
@abstract_request
@auth_deco
def ping_pong(req):
    return("pong", 200)


@app.route("/crawl", methods=["POST"])
@abstract_request
@auth_deco
def crawl(req):
    global file_worker
    global news_sentiment
    global KST
    global target_lang
    global logger

    utc_now = datetime.datetime.utcnow()
    kst = pytz.utc.localize(utc_now).astimezone(KST)
    try:
        # post 메시지 파싱
        recevied_msg = json.loads(req.get_data().decode("utf-8"))
        subject = recevied_msg["subject"]
        source_lang = recevied_msg["source_lang"]

        header_crawler = HeaderCrawler(target_lang)

        # db worker 객체 생성
        db_worker = DBworker(database=subject, collection=source_lang, kst=kst)

        eng_headers, translated_headers = header_crawler.get_news_header(subject)

        sentiment_results = list()
        for header in eng_headers:
            res = news_sentiment.pred(header)
            sentiment_results.append(res)

        file_worker.upload_result(eng_headers, translated_headers, source_lang, subject, kst, sentiment_results)
        db_worker.save_result(sentiment_results)

        return("ok", 200)
    except Exception:
        error = traceback.format_exc()
        error = pretty_trackback(error)
        logger.error_log(error)
        return(error, 400)


if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=8080, debug=False)