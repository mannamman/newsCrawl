import pymongo
## local 테스트 ##
# from dotenv import load_dotenv
import os
import pytz
import datetime
import itertools
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
    def __init__(self, database :str, collection :str):
        ## local 테스트 ##
        # load_dotenv(dotenv_path=f"{os.getcwd()}/cred/.mongopasswd",verbose=True)
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
        KST = pytz.timezone("Asia/Seoul")
        utc_now = datetime.datetime.utcnow()
        kst = pytz.utc.localize(utc_now).astimezone(KST)
        sec = kst.second
        ms = kst.microsecond
        dt = datetime.timedelta(microseconds=ms, seconds=sec)
        self.kst = kst - dt


    def __merge_result(self, results :list) -> defaultdict:
        merged_result = list(itertools.chain(*results))
        word_dic = defaultdict(int)
        for word in merged_result:
            word_dic[word] += 1
        return word_dic


    def save_result(self, results :list):
        word_dic = self.__merge_result(results)
        ## local 테스트 ##
        # print(word_dic)
        # return

        ## 배포시 사용 ##
        doc_format = {
            "createdAt" : self.kst,
            "words" : word_dic
        }
        self.collection.insert_one(doc_format)


    # subject.error.yyyymmdd_hhmm
    def save_error(self, contexts :list):
        try:
            contexts = list(itertools.chain(*contexts))
            contexts = [str(word) for word in contexts]
            contexts = ", ".join(contexts)
        except TypeError as e:
            contexts = f"TypeError {e}"
        except Exception as e:
            contexts = f"anyException {e}"
        doc_format = {
            "createdAt" : self.kst,
            "context" : contexts
        }
        self.error_collection.insert_one(doc_format)