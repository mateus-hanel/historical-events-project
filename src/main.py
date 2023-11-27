from MongoConnector import MongoConnector
from datetime import datetime
from flask import Flask, render_template, request
import json

app = Flask(__name__, template_folder="template")

connector = MongoConnector("mongodb://localhost:27017/", "src/queries/queries.json")
connector.insert_historical_data()
connector.create_events_formatted_date_collection()


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "GET":
        lower_date = datetime(2010, 1, 1)
        upper_date = datetime(2020, 12, 31)
    if request.method == "POST":
        parameters = request.form
        keys = parameters.keys()
        parameters_place = [
            parameters[place] for place in keys if place.startswith("place")
        ]
        parameters_topic = [
            parameters[topic] for topic in keys if topic.startswith("topic")
        ]

        print(parameters_place)
        print(parameters_topic)

        lower_date = datetime.strptime(parameters["date-start"], "%Y-%m-%d")
        upper_date = datetime.strptime(parameters["date-end"], "%Y-%m-%d")
    df = connector.filter_date(lower_date, upper_date)

    list_places, list_topics = connector.get_categories()

    return render_template(
        "simple.html",
        tables=[df.to_html(classes="data")],
        titles=df.columns.values,
        list_places=list_places,
        list_places_len=len(list_places),
        list_topics=list_topics,
        list_topics_len=len(list_topics),
        date_start="2010-01-01",
        date_end="2020-12-31",
    )


if __name__ == "__main__":
    app.run()
