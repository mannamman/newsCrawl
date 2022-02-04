from modules.newsCrawler import HeaderCrawler
from modules.mongo_db import DBworker
from modules.file_worker import FileWorker
from modules.req_valid import auth_deco
from modules.log_module import Logger
from finBERT.sentiment import FinBert
import pytz
import datetime
import json
import functools
from math import ceil
import os
import traceback
import copy
# multi process
from multiprocessing import Pool


# server
from flask import request, Flask

app = Flask(__name__)

# 객체 초기화(공통으로 사용되는)
file_worker = FileWorker()
sentiment_finbert = None
logger = Logger()


KST = pytz.timezone("Asia/Seoul")

def init_sentiment():
    global sentiment_finbert
    sentiment_finbert = FinBert()


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


def crawl(subject :str, source_lang :str) -> tuple:
    # get urls
    # contury code
    header_crawler = HeaderCrawler(source_lang)
    origin_headers, translated_headers, news_links = header_crawler.get_news_header(subject)
    return origin_headers, translated_headers, news_links


def sentiment_analysis_fin(*args):
    global sentiment_finbert

    process_id, header, news_link = args[0]
    res = sentiment_finbert.pred(header)
    # print(f"process {process_id} : {res}")
    res["url"] = news_link
    return res


def make_chunk(headers :list, headers_len :int, cpu_count :int) -> list:
    return list(
        map(
            lambda x: headers[x*cpu_count:x*cpu_count+cpu_count],
            [i for i in range(ceil(headers_len/cpu_count))]
        )
    )


def save_result(
        subject :str, source_lang :str, origin_headers :list,
        translated_headers :list, kst :datetime.datetime,
        sentiment_results :list
    ):
    global file_worker

    db_worker = DBworker(database=subject, collection=source_lang, kst=kst)

    # 결과 및 원본을 스토리지에 저장
    # 경로는 subject/source_lang/kst
    file_worker.upload_result(origin_headers, translated_headers, source_lang, subject, kst, sentiment_results)

    # mongo에 결과 저장
    db_worker.save_result(sentiment_results)


@app.route("/sentiment", methods=["GET", "POST"])
@abstract_request
@auth_deco
def index(req):
    global KST
    global logger
    global sentiment_finbert

    # 헬스 체크
    if(req.method == "GET"):
        return("pong", 200)

    # lazy loading
    if(sentiment_finbert is None):
        init_sentiment()

    try:
        # post 메시지 파싱
        recevied_msg = json.loads(req.get_data().decode("utf-8"))
        subject = recevied_msg["subject"]
        source_lang = recevied_msg["source_lang"]

        utc_now = datetime.datetime.utcnow()
        kst = pytz.utc.localize(utc_now).astimezone(KST)

        # news header만 수집(source가 en이 아니라면 번역)
        origin_headers, translated_headers, news_links = crawl(subject, source_lang)

        headers_len = len(origin_headers)
        sentiment_results = list()
        cpu_count = os.cpu_count()

        # source가 en이라면
        if(translated_headers is None):
            translated_headers = origin_headers

        translated_headers_copy = copy.copy(translated_headers)
        translated_headers_copy = [(idx+1, header, news_link) for idx, (header, news_link) in enumerate(zip(translated_headers_copy, news_links))]

        # cpu만큼의 프로세스를 동작시키기 위해
        chunks = make_chunk(translated_headers_copy, headers_len, cpu_count)

        for chunk_idx, chunk in enumerate(chunks):
            pool_len = len(chunk)
            with Pool(pool_len) as pool:
                res = pool.map(sentiment_analysis_fin, chunk)
                sentiment_results.extend(res)

        save_result(subject, source_lang, origin_headers, translated_headers, kst, sentiment_results)
        return("ok", 200)

    except Exception:
        error = traceback.format_exc()
        error = pretty_trackback(error)
        logger.error_log(error)
        return(error, 400)


if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=8080, debug=False)
    