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

class BaseWorker:
    def __init__(self):
        ## local 테스트 ##
        dot_env_path = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(dotenv_path=f"{dot_env_path}/../cred/.mongopasswd",verbose=True)
        ip = os.getenv("ip")
        port = os.getenv("port")
        user = os.getenv("user")
        passwd = os.getenv("passwd")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")

class newWorker(BaseWorker):
    def __init__(self):
        super().__init__()
        self.db = self.client["stock"]
        self.collection = self.db["en"]

    def insert_regacy(self, results, subject):
        for result in results:
            result["subject"] = subject
            self.collection.insert_one(result)

    def migration_for_mistyping(self):
        self.collection.update_many({ "subejct": { "$exists": True } }, { "$rename": { 'subejct': 'subject'} })


class regacyWorker(BaseWorker):
    def __init__(self, dbname: str, collection: str):
        super().__init__()
        self.db = self.client[dbname]
        self.collection = self.db[collection]

    def get_all_data(self, subejct):
        res = self.collection.find()
        filterd_res = list()
        for r in res:
            if("url" in r["sentiment"][0]):
                filterd_res.append(r)
        print(subject, len(filterd_res))
        return filterd_res

if(__name__ == "__main__"):
    new_db_worker = newWorker()
    new_db_worker.migration_for_mistyping()