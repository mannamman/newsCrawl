from newsCrawler import Crawler
from translater import Translater
from mongo_db import DBworker

subject = "snp500"
source_lang = "en"
# 아직 번역 api를 사용하지 않으므로
target_lang = "en"

def index(request):
    global subject
    global source_lang
    global target_lang
    crawler = Crawler(source_lang)
    contexts = crawler.crawl(subject)
    translater = Translater(source_lang, target_lang, len(contexts), contexts)
    results = translater.translate()
    db_worker = DBworker(database=subject, collection=target_lang)
    db_worker.save_result(results)
    return("ok", 200)

if(__name__ == "__main__"):
    index(None)