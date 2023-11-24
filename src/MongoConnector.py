import json
from pymongo import MongoClient
from data.MongoInserter import MongoInserter


class MongoConnector:
    def __init__(self, connection_path: str):
        self.connection_path = connection_path
        self.client = MongoClient(self.connection_path)
        self.db = self.client["historical_events"]
        self.db = None
        self.inserter = MongoInserter(self.client, "historical_events")

    def insert_historical_data(self):
        self.inserter .insert_data_from_file(
            "data/formatted_historical_events.json", "events")


if __name__ == "__main__":

    connector = MongoConnector("mongodb://localhost:27017/")
    connector.insert_historical_data()
