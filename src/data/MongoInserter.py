import json
from pymongo import MongoClient


class MongoInserter:
    def __init__(self, client: MongoClient, database: str):
        self.client = client
        self.db = self.client[database]

    def is_collection_created(self, collection_name):
        list_of_collections = self.db.list_collection_names()
        return collection_name in list_of_collections

    def insert_data_from_file(self, json_path: str, collection_name: str):
        if self.is_collection_created(collection_name):
            print("Data already imported")
            return
        print("Importing Data...")
        with open(json_path, encoding="utf8") as f:
            content = f.read()
            file_data = json.loads(content)
            print(type(file_data))
            self.db[collection_name].insert_many(file_data)
        print("Data Imported")
