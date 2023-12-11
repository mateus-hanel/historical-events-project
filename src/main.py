from MongoConnector import MongoConnector
from datetime import datetime
from flask import Flask, render_template, request
import json

app = Flask(__name__, template_folder="template")

connector = MongoConnector("mongodb://localhost:27017/", "src/queries/queries.json")
connector.insert_historical_data()
connector.create_events_formatted_date_collection()
list_places, list_topics = connector.get_categories()


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "GET":
        parameters = {}
        parameters["date-start"] = "0100-01-01"
        parameters["date-end"] = "0300-12-31"
        parameters_place = []
        parameters_topic = []

    if request.method == "POST":
        parameters = request.form
        keys = parameters.keys()
        parameters_place = [
            parameters[place] for place in keys if place.startswith("place")
        ]
        parameters_topic = [
            parameters[topic] for topic in keys if topic.startswith("topic")
        ]

    lower_date = datetime.strptime(parameters["date-start"], "%Y-%m-%d")
    upper_date = datetime.strptime(parameters["date-end"], "%Y-%m-%d")
    df = connector.filter_data(
        lower_date, upper_date, parameters_place, parameters_topic
    )

    return render_template(
        "simple.html",
        tables=[df.to_html(classes="data")],
        titles=df.columns.values,
        list_places=list_places,
        list_places_len=len(list_places),
        list_topics=list_topics,
        list_topics_len=len(list_topics),
        date_start=parameters["date-start"],
        date_end=parameters["date-end"],
    )


if __name__ == "__main__":
    app.run()
