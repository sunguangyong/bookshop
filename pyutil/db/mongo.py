#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
 
import pymongo  
import datetime  
from bson.objectid import ObjectId  
   
class mongo:
    def __init__(self, config):  
        self.client = pymongo.MongoClient(config["host"], config["port"])
        self.db = self.client[config["database"]]
        print "_________________//////////////"


    def __filter_objectid(self, items, json):
        if json==True and items:
            for item in items:
                del item["_id"]
        return list(items)

       
    def insert(self, tableName, item):
        id = self.db[tableName].insert(item)  
        return id


    def insert_multi(self, tableName, items):  
        id = self.db[tableName].insert(items)  
        return id


    def get(self, tableName, indexMap={}, orderby=(), json=True):
        items = list(self.db[tableName].find(indexMap))
        return self.__filter_objectid(items, json)

   
    def get_one(self, tableName, indexMap={}, json=True):
        item = self.db[tableName].find_one(indexMap)
        return self.__filter_objectid(item)

   
    def get_by_objectid(self, tableName, objectid, json=True):  
        item = self.db[tableName].find_one({"_id": ObjectId(str(objectid))})  
        return self.__filter_objectid(item, json)


    def columns(self, tableName):
        return self.get_one(tableName).keys()
       

    def update(self, tableName, dataMap, indexMap): 
        print "test 1"
        item = self.db[tableName].update(indexMap)
        print "test 2"
        return self.__filter_objectid(item, json)


    def count(self, tableName, indexMap):
        if not indexMap:
            return self.db[tableName].count()  
        else:
            return len(self.get(tableName, indexMap))
       

    def remove(self, tableName, indexMap):  
        self.db[tableName].remove(indexMap)


    def clear(self, tableName):
        self.collection.remove()  


def test():
    import pyconf.db.manna_mongo as manna_mongo
    mog = mongo(manna_mongo.config)
    id = mog.insert("qiuzi", {"a":12, "b":333})
    print id
    print mog.get_by_id("qiuzi", id)
    print "--------------"

    ids = mog.insert("qiuzi", [{"a":12, "b":333}, {"x":0, "y":999}])
    print ids

    print mog.get("qiuzi")
   

if __name__ == '__main__':  
    test()
