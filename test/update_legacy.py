import pymongo
## local 테스트 ##
from dotenv import load_dotenv
import os
import pytz
import datetime
from uuid import uuid4
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
        load_dotenv(dotenv_path=f"{os.getcwd()}/../cred/.mongopasswd",verbose=True)
        ip = os.getenv("ip")
        port = os.getenv("port")
        user = os.getenv("user")
        passwd = os.getenv("passwd")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # db 설정
        self.db = self.client[database]
        # table 고정(collection)
        self.collection = self.db[collection]

    def strKst_to_datetimeKst(self):
        result = self.collection.find()
        dt = datetime.timedelta(hours=9)
        for r in result:
            uniq_k = r["createdAt"]
            k = r["createdAt"]
            if(not isinstance(k, datetime.datetime)):
                k = datetime.datetime.strptime(k, "%Y%m%d_%H%M")
                k = k - dt
                k = pytz.utc.localize(k)
                r["createdAt"] = k
                r["uuid"] = uuid4()
                self.collection.update_one({"createdAt" : uniq_k}, {"$set" : r})
                
    
    def test_delete_one(self):
        self.collection.delete_one({"_id" : ObjectId("61de741789c23b2942717dd1")})

    def test_find_all(self):
        result = self.collection.find()
        for r in result:
            print(r["createdAt"], r["uuid"])

if(__name__ == "__main__"):
    worker = DBworker("tesla", "ko")
    worker.strKst_to_datetimeKst()
    worker.test_find_all()