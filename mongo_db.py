import pymongo
from dotenv import load_dotenv
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
        load_dotenv(dotenv_path=f"{os.getcwd()}/cred/.mongopasswd",verbose=True)
        ip = os.getenv("ip")
        port = os.getenv("port")
        user = os.getenv("user")
        passwd = os.getenv("passwd")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # db 설정
        self.db = self.client[database]
        # table 고정(collection)
        self.collection = self.db[collection]
        # 저장되는 시간 설정
        KST = pytz.timezone("Asia/Seoul")
        utc_now = datetime.datetime.utcnow()
        kst = pytz.utc.localize(utc_now).astimezone(KST)
        self.kst = kst.strftime("%Y%m%d_%H%M")


    def __merge_result(self, results :list) -> defaultdict:
        merged_result = list(itertools.chain(*results))
        word_dic = defaultdict(int)
        for word in merged_result:
            word_dic[word] += 1
        return word_dic


    def save_result(self, results :list):
        word_dic = self.__merge_result(results)
        doc_format = {
            "createdAt" : self.kst,
            "words" : word_dic
        }
        self.collection.insert_one(doc_format)