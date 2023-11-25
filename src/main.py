from MongoConnector import MongoConnector
from datetime import datetime

if __name__ == "__main__":
    connector = MongoConnector("mongodb://localhost:27017/", "src/queries/queries.json")
    connector.insert_historical_data()
    connector.create_events_formatted_date_collection()

    lower_date = datetime(1000, 1, 1, 3, 6, 28)
    upper_date = datetime(1001, 1, 1, 3, 6, 28)

    connector.filter_date(lower_date, upper_date)
