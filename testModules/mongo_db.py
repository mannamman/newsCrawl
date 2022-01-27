import pymongo
## local 테스트 ##
from dotenv import load_dotenv
import os
import pytz
import datetime
import itertools
from uuid import uuid4
from collections import defaultdict
# ObjectId로 쿼리할때 필요
from bson.objectid import ObjectId

"""
RDBMS	    Mongo DB
Database	Database
Table	    Collection
Row	        Document
Index	    Index
DB server	Mongod
DB client	mongo
"""

class DBworker:
    def __init__(self, database :str, collection :str , kst :datetime.datetime):
        ## local 테스트 ##
        dot_env_path = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(dotenv_path=f"{dot_env_path}/../cred/.mongopasswd",verbose=True)
        ip = os.getenv("ip")
        port = os.getenv("port")
        user = os.getenv("user")
        passwd = os.getenv("passwd")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # db 설정
        self.db = self.client[database]
        # table 고정(collection)
        self.collection = self.db[collection]
        # error가 발생한 단어들을 저장할 컬렉션
        self.error_collection = self.db["ERROR"]
        # 저장되는 시간 설정
        # KST = pytz.timezone("Asia/Seoul")
        # utc_now = datetime.datetime.utcnow()
        # kst = pytz.utc.localize(utc_now).astimezone(KST)
        sec = kst.second
        ms = kst.microsecond
        dt = datetime.timedelta(microseconds=ms, seconds=sec)
        self.kst = kst - dt


    def save_result(self, sentiment_results :list):
        ## local 테스트 ##
        # print(word_dic)
        # return

        ## 배포시 사용 ##
        doc_format = {
            "uuid" : uuid4(),
            "createdAt" : self.kst,
            "sentiment" : sentiment_results
        }
        self.collection.insert_one(doc_format)


    # # subject.error.yyyymmdd_hhmm
    # def save_error(self, contexts :list):
    #     try:
    #         contexts = list(itertools.chain(*contexts))
    #         contexts = [str(word) for word in contexts]
    #         contexts = ", ".join(contexts)
    #     except TypeError as e:
    #         contexts = f"TypeError {e}"
    #     except Exception as e:
    #         contexts = f"anyException {e}"
    #     doc_format = {
    #         "createdAt" : self.kst,
    #         "context" : contexts
    #     }
    #     self.error_collection.insert_one(doc_format)