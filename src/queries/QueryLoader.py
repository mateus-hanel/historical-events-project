import json
import os


class QueryLoader:
    def __init__(self, path: str):
        with open(path, "r", encoding="utf8") as file:
            self.queries = json.load(file)

    def get_queries(self):
        return self.queries
