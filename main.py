from newsCrawler import Crawler, UrlMaker
from translater import Translater
from mongo_db import DBworker
from threading import Thread


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


subject = "snp500"
source_lang = "en"
target_lang = "en"
# 아직 번역 api를 사용하지 않으므로
api = False



def index(request):
    global subject
    global source_lang
    global target_lang
    global api

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

if(__name__ == "__main__"):
    index(None)