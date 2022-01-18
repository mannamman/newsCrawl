from testModules.newsCrawler import Crawler, UrlMaker, NltkWorker
from testModules.translater import Translater
from testModules.mongo_db import DBworker
from testModules.file_worker import FileWorker
from threading import Thread
import json
import functools
# log
import traceback
import time

# 객체 초기화(공통으로 사용되는)
crawler = Crawler()
nltk_worker = NltkWorker()
translater = Translater()
file_worker = FileWorker()


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
    global nltk_worker
    print(f"thread {idx} start")
    context = crawler.crawl(url)
    if(context == ""):
        print(f"thread {idx} fail")
        context_results[idx] = ""
        return
    context_results[idx] = nltk_worker.preprocess(context)
    print(f"thread {idx} done")

def crawl():
    global crawler
    global translater
    global file_worker

    start = time.time()
    try:
        subject = "snp500"
        source_lang = "en"
        target_lang = "ko"

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
        input_uri, output_uri = file_worker.save_and_upload(context_results)
        translater.batch_translate(source_lang, target_lang, input_uri, output_uri)
        # db_worker.save_result(context_results)
        print(round((time.time() - start), 2))
        return("ok", 200)
    except Exception:
        error = traceback.format_exc()
        error = pretty_trackback(error)
        return(error, 400)


if(__name__ == "__main__"):
    crawl()