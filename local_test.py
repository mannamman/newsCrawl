from testModules.newsCrawler import HeaderCrawler
from testModules.mongo_db import DBworker
from testModules.file_worker import FileWorker
from sentiment_dir.sentiment import NewsSentiment
import pytz
import datetime
import json
import functools
# log
import traceback
import time

# 객체 초기화(공통으로 사용되는)
file_worker = FileWorker()
news_sentiment = NewsSentiment()

KST = pytz.timezone("Asia/Seoul")


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


def crawl():
    global file_worker
    global news_sentiment
    global KST

    start = time.time()
    utc_now = datetime.datetime.utcnow()
    kst = pytz.utc.localize(utc_now).astimezone(KST)
    try:
        subject = "snp500"
        source_lang = "en"
        # print(kst.strftime("%Y-%m-%d_%H:%M:00"))

        # get urls
        header_crawler = HeaderCrawler("en")

        # db worker 객체 생성
        db_worker = DBworker(database=subject, collection=source_lang, kst=kst)

        eng_headers, translated_headers = header_crawler.get_news_header(subject)

        sentiment_results = list()
        for header in eng_headers:
            res = news_sentiment.pred(header)
            sentiment_results.append(res)

        print(sentiment_results)
        # file_worker.upload_result(eng_headers, translated_headers, source_lang, subject, kst, sentiment_results)
        # db_worker.save_result(sentiment_results)
        print(round((time.time() - start), 2))
        return("ok", 200)
    except Exception:
        error = traceback.format_exc()
        error = pretty_trackback(error)
        print(error)
        return(error, 400)


if(__name__ == "__main__"):
    crawl()