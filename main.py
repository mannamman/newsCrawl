from modules.newsCrawler import HeaderCrawler
from modules.mongo_db import DBworker
from modules.file_worker import FileWorker
from modules.log_module import Logger
from finBERT.sentiment import FinBert
import pytz
import datetime
import functools
from math import ceil
import os
import traceback
import copy
from typing import Tuple, List, Dict
from uuid import uuid4
from flask import Response
# multi process
from multiprocessing import Pool


# server
from flask import request, Flask

app = Flask(__name__)

# 객체 초기화(공통으로 사용되는)
db_worker = DBworker()
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


def pretty_trackback(msg: str) -> str:
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


def crawl(subject :str, source_lang :str) -> Tuple[List[str], List[str], List[str]]:
    # get urls
    # contury code
    header_crawler = HeaderCrawler(source_lang)
    origin_headers, translated_headers, news_links = header_crawler.get_news_header(subject)
    return origin_headers, translated_headers, news_links


def sentiment_analysis_fin(*args) -> Dict[str,any]:
    global sentiment_finbert

    process_id, header, news_link = args[0]
    res = sentiment_finbert.pred(header)
    # print(f"process {process_id} : {res}")
    res["url"] = news_link
    return res


def make_chunk(headers: List[str], headers_len: int, cpu_count: int) -> List[List[str]]:
    return list(
        map(
            lambda x: headers[x*cpu_count:x*cpu_count+cpu_count],
            [i for i in range(ceil(headers_len/cpu_count))]
        )
    )


def save_result(
        subject: str, source_lang: str, origin_headers: List[str],
        translated_headers: List[str], kst: datetime.datetime,
        sentiment_results: List[str]
    ):
    global file_worker
    global db_worker

    # 결과 및 원본을 스토리지에 저장
    # 경로는 subject/source_lang/kst
    file_worker.upload_result(origin_headers, translated_headers, source_lang, subject, kst, sentiment_results)

    # mongo에 결과 저장
    db_worker.save_result(sentiment_results, subject, kst)


@app.route("/sentiment", methods=["GET"])
def index():
    global KST
    global logger
    global sentiment_finbert
    global db_worker

    # lazy loading
    if(sentiment_finbert is None):
        init_sentiment()

    try:
        stock_list = db_worker.get_stock_list()
        # 일단 영어로 고정
        source_lang = "en"

        for subject in stock_list:
            kst_start = pytz.utc.localize(datetime.datetime.utcnow()).astimezone(KST)

            cur_job_uuid = uuid4()
            logger.debug_log(f"<{str(cur_job_uuid)}> start {subject} at {kst_start}")

            # news header만 수집(source_lang en이 아니라면 번역)
            origin_headers, translated_headers, news_links = crawl(subject, source_lang)

            headers_len = len(origin_headers)
            sentiment_results = list()
            cpu_count = os.cpu_count()

            # source_lang en이라면
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

            kst_end = pytz.utc.localize(datetime.datetime.utcnow()).astimezone(KST)
            # save_result(subject, source_lang, origin_headers, translated_headers, kst_end, sentiment_results)
            logger.debug_log(f"<{str(cur_job_uuid)}> done {subject} at {kst_end}")

        return Response(response="ok", status=200)

    except Exception:
        error = traceback.format_exc()
        error = pretty_trackback(error)
        logger.error_log(error)
        return Response(response=error, status=400)


if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=8080, debug=False)
    