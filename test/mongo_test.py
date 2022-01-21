import pymongo
from dotenv import load_dotenv
import os
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


# database = "tesla"
# collections = "ko"

class DBworker:
    def __init__(self, database="google", collections="ko"):
        # global database
        # global collections
        dot_env_path = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(dotenv_path=f"{dot_env_path}/../cred/.mongopasswd" ,verbose=True)
        ip = os.getenv("ip")
        port = os.getenv("port")
        user = os.getenv("user")
        passwd = os.getenv("passwd")
        self.client = pymongo.MongoClient(f"mongodb://{user}:{passwd}@{ip}:{port}/")
        # db 설정
        self.db = self.client[database]
        # table 고정(collection)
        self.collection = self.db[collections]


    def test_insert_one(self, name :str, context :str):
        self.collection.insert_one({"user" : name, "context" : context})


    def test_insert_many(self, users :list):
        self.collection.insert_many(users)


    def test_find_one(self):
        # result = self.collection.find_one()
        # result = self.collection.find_one({"user" : "user"})
        # result = self.collection.find_one({"20212511_1420" :{ "$exists" : "true" }})
        result = self.collection.find_one({"createdAt" : "bccdef"})
        print(result)

    def test_find_one_createdAt(self, createdAt):
        result = self.collection.find_one({"createdAt" : createdAt})
        print(result)


    def test_find_many(self):
        result = self.collection.find({"user" : "user"})
        while True:
            try:
                print(result.next())
            except StopIteration:
                break
            


    def test_find_all(self):
        result = self.collection.find()
        for r in result:
            if("sentiment" not in r):
                continue
            print(r["createdAt"], r["sentiment"])


    def test_update(self):
        # result = self.collection.update_one({"_id" : ObjectId("619750507eabfd1c8ba0f89c")}, {"$set":{"user" : "you", "context" : "first name is you"}})
        result = self.collection.update_one({"user" : "user"}, {"$set":{"user" : "user", "context" : "first name is nam"}})
        print(result)
        


    def test_count_doc(self):
        # all_doc_count = self.collection.count_documents({})
        # print(all_doc_count)
        doc_count = self.collection.count_documents({"20212511_1420" :{ "$exists" : "true" }})
        print(doc_count)


    def test_remove_all(self):
        # 모두 삭제
        self.collection.remove()
        # 조건에 맞는 모든 문서 삭제
        # self.colletion.remove({"user" : "kim"})


    def test_delete_one(self):
        self.collection.delete_one({"createdAt" : "20211220_1454"})
    
    def test_delete_one_id(self, _id):
        self.collection.delete_one({"_id" : ObjectId(_id)})

    def test_delete_many(self):
        self.collection.delete_many({"user" : "user"})

if(__name__ == "__main__"):
    db = DBworker()
    db.test_find_all()
    # db.test_find_one_createdAt("20211227_0900")
    # db.test_find_one()
    # db.test_remove_all()