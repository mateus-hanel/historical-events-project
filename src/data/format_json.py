"""
This file changes the raw data at data/historical_events.json into a better format for importing. This is necessary because the original file has several fields with the same name (event)
"""
import json
import codecs


if __name__ == "__main__":
    with open("data/historical_events_replaced.json", encoding='utf-8') as f:
        original = json.load(f)
        original = original["result"]
        del original['count']
        only_values = list(original.values())
        print(only_values[0])
        with open('data/formatted_historical_events.json', 'w', encoding='utf8') as file:
            json.dump(only_values, file, indent=4)
