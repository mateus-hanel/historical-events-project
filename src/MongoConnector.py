import json
from pymongo import MongoClient
from data.MongoInserter import MongoInserter
from queries.QueryLoader import QueryLoader
from datetime import datetime
import pandas as pd


class MongoConnector:
    def __init__(self, connection_path: str, queries_path: str):
        self.connection_path = connection_path
        self.client = MongoClient(self.connection_path)
        self.db = self.client["historical_events"]
        self.inserter = MongoInserter(self.client, "historical_events")
        query_loader = QueryLoader(queries_path)
        self.queries = query_loader.get_queries()
        return

    def insert_historical_data(self):
        self.inserter.insert_data_from_file(
            "data/formatted_historical_events.json", "events"
        )
        return

    def create_events_formatted_date_collection(self):
        print("Creating events_formatted_date collection...")
        pipeline = self.queries["pipeline_convert_date"]
        self.db["events"].aggregate(pipeline)
        print("Collection created")
        return

    def filter_data(self, lower_date, upper_date, parameters_place, parameters_topic):
        query_date = self.queries["date_filter"]
        fields = self.queries["date_filter_fields"]

        query_date["$and"][0]["date_formatted"]["$gte"] = lower_date
        query_date["$and"][1]["date_formatted"]["$lte"] = upper_date

        categories = parameters_place + parameters_topic

        if categories:
            query_category = self.queries["query_category"]
            query_category["category2"]["$in"] = categories
        else:
            query_category = {}

        query_and = self.queries["query_and"]
        query_and["$and"][0] = query_date
        query_and["$and"][1] = query_category

        print(query_and)
        # quit()
        cursor = self.db["events_formatted_date"].find(query_and, fields)

        df = pd.DataFrame(list(cursor))
        # df = df.drop("_id", axis=1)

        return df

    def filter_date(self, lower_date, upper_date):
        query = self.queries["date_filter"]
        fields = self.queries["date_filter_fields"]
        query["$and"][0]["date_formatted"]["$gte"] = lower_date
        query["$and"][1]["date_formatted"]["$lte"] = upper_date

        cursor = self.db["events_formatted_date"].find(query, fields)

        df = pd.DataFrame(list(cursor))
        df = df.drop("_id", axis=1)
        return df

    def get_categories(self):
        pipeline = self.queries["pipeline_get_categories"]
        categories = list(self.db["events_formatted_date"].aggregate(pipeline))
        list_places = categories[0]["categories"]
        list_places = [s.strip("=") for s in list_places]
        list_places.sort()
        list_topics = categories[1]["categories"]
        list_topics.sort()
        return list_places, list_topics


if __name__ == "__main__":
    connector = MongoConnector("mongodb://localhost:27017/", "src/queries/queries.json")
    connector.insert_historical_data()
    connector.create_events_formatted_date_collection()

    lower_date = datetime(1, 1, 1, 3, 6, 28)
    upper_date = datetime(1001, 1, 1, 3, 6, 28)

    # data = connector.filter_data(lower_date, upper_date, ["China"], ["Roman Empire"])
    data = connector.filter_data(lower_date, upper_date, [], [])

    print(data.head())
