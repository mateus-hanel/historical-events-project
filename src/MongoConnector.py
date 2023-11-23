import json
from pymongo import MongoClient


class MongoConnector:
    def __init__(self, connection_path):
        self.connection_path = connection_path

    def connect(self):
        self.client = MongoClient(self.connection_path)
        self.db = self.client["historical_events"]

    def is_collection_created(self, collection_name):
        list_of_collections = self.db.list_collection_names()
        return collection_name in list_of_collections

    def insert_data_from_file(self, json_path):
        if self.is_collection_created("events"):
            print("Data already imported")
            return
        print("Importing Data...")
        with open(json_path, encoding='utf8') as f:
            content = f.read()
            file_data = json.loads(content)
            print(type(file_data))
            self.db["events"].insert_many(file_data)
        print("Data Imported")


if __name__ == "__main__":
    connector = MongoConnector("mongodb://localhost:27017/")
    connector.connect()
    connector.insert_data_from_file("data/formatted_historical_events.json")
