import pymongo
import os
import datetime
from uuid import uuid4
from typing import Dict, List

class DBworker:
    def __init__(self):
        ip = os.getenv("ip")
        port = os.getenv("port")
        user = os.getenv("user")
        passwd = os.getenv("passwd")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # db 설정
        self.db = self.client["stock"]
        self.collection = self.db["en"]
        # stock list
        self.stock_list_collection = self.db["stockList"]

    def get_stock_list(self) -> List[str]:
        cursor = self.stock_list_collection.find()
        stock_list = []
        for doc in cursor:
            stock_name = doc["stock_name"]
            stock_list.append(stock_name)
        return stock_list

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
            "subject" : subject,
            "createdAt" : rounded_kst,
            "sentiment" : sentiment_results
        }

        self.collection.insert_one(doc_format)
