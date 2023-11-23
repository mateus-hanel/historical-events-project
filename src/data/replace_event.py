import json


def replace_event(data):
    search_text = '"event'
    replace_text = '"historical_'
    n_replaced = 0
    index = 0

    chunks = []
    while True:

        print(n_replaced)
        index = data.find(search_text)
        if index == -1:
            break
        replace_text_counter = f"{replace_text}{n_replaced}"
        chunks.append(data[:index])
        data = data[index:].replace(search_text, replace_text_counter, 1)
        n_replaced += 1
    chunks.append(data)
    return "".join(chunks)


if __name__ == "__main__":
    with open("data/historical_events.json", encoding='utf-8') as f:
        original = f.read()
        original_replaced = replace_event(original)
        json_replaced = json.loads(original_replaced)
        with open('data/historical_events_replaced.json', 'w', encoding='utf8') as file:
            json.dump(json_replaced, file)

        print(original)
