from testModules.newsCrawler import HeaderCrawler
from testModules.mongo_db import DBworker
from testModules.file_worker import FileWorker
from finBERT.sentiment import FinBert
import pytz
import datetime
import json
import functools
# log
import traceback
import time
# multi process
from math import ceil
from multiprocessing import Pool
import os
import copy

# 객체 초기화(공통으로 사용되는)
file_worker = FileWorker()
sentiment_finbert = FinBert()

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


def make_chunk(headers, headers_len, cpu_count):
    return list(
        map(
            lambda x: headers[x*cpu_count:x*cpu_count+cpu_count],
            [i for i in range(ceil(headers_len/cpu_count))]
        )
    )


def save_result(subject, source_lang, origin_headers, translated_headers, kst, sentiment_results):
    global file_worker

    db_worker = DBworker(database=subject, collection=source_lang, kst=kst)

    file_worker.upload_result(origin_headers, translated_headers, source_lang, subject, kst, sentiment_results)

    db_worker.save_result(sentiment_results)


if(__name__ == "__main__"):
    subject = "snp500"
    source_lang = "en"

    utc_now = datetime.datetime.utcnow()
    kst = pytz.utc.localize(utc_now).astimezone(KST)

    origin_headers, translated_headers, news_links = crawl(subject, source_lang)

    headers_len = len(origin_headers)
    sentiment_results = list()
    cpu_count = os.cpu_count()

    if(translated_headers is None):
        translated_headers = origin_headers

    translated_headers_copy = copy.copy(translated_headers)
    translated_headers_copy = [(idx+1, header, news_link) for idx, (header, news_link) in enumerate(zip(translated_headers_copy, news_links))]
    chunks = make_chunk(translated_headers_copy, headers_len, cpu_count)

    for chunk_idx, chunk in enumerate(chunks):
        pool_len = len(chunk)
        with Pool(pool_len) as pool:
            res = pool.map(sentiment_analysis_fin, chunk)
            sentiment_results.extend(res)
        break
    # print(sentiment_results)
    # save_result(subject, source_lang, origin_headers, translated_headers, kst, sentiment_results)

    