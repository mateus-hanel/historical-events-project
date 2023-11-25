import json
import os


class QueryLoader:
    def __init__(self, path: str):
        with open(path, "r", encoding="utf8") as file:
            self.queries = json.load(file)

    def get_queries(self):
        return self.queries


test = {
    "date_filter_fields": {
        "date_formatted": 1,
        "description": 1,
        "category1": 1,
        "category2": 1,
    }
}
