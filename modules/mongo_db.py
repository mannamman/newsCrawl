import pymongo
import os
import datetime
from uuid import uuid4
from typing import Dict, List
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
    def __init__(self):
        ip = os.getenv("ip")
        port = os.getenv("port")
        user = os.getenv("user")
        passwd = os.getenv("passwd")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # db 설정
        self.db = self.client["stock"]
        # table 고정(collection)
        self.collection = self.db["en"]

    def save_result(
            self,
            sentiment_results: List[Dict[str,any]],
            subject: str,
            kst: datetime.datetime
        ) -> None:

        sec = kst.second
        ms = kst.microsecond
        dt = datetime.timedelta(microseconds=ms, seconds=sec)
        rounded_kst = kst - dt

        doc_format = {
            "uuid" : uuid4(),
            "subejct" : subject,
            "createdAt" : rounded_kst,
            "sentiment" : sentiment_results
        }

        self.collection.insert_one(doc_format)
