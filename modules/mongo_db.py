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
