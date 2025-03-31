import json
import sys
import requests
import time
import os

counter = 0
keep_fetching = True

def fetch_wolt_data(id):
    global counter
    response = requests.get(create_url_from_id(id))
    data = response.json()
    counter += 1
    file_name = f"out/wolt_{id}_{counter}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Wrote to {file_name}")
    interval = data['refresh_in_seconds'] if 'refresh_in_seconds' in data else 30
    return interval

def split_url(url: str):
    # https://track.wolt.com/hu/s/8T8XYgUlfUsOdDEb8vipxQ
    parts = url.split("/")
    return parts[-1]

def create_url_from_id(id):
    return f"https://consumer-api.wolt.com/order-tracking-api/v1/details/tracking-code/track/{id}"

def main():
    global counter
    global keep_fetching

    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        exit(1)

    id = split_url(sys.argv[1])
    os.makedirs("out", exist_ok=True)
    while keep_fetching:
        interval = fetch_wolt_data(id)
        if interval == 0:
            keep_fetching = False
            continue

        print(f"Will sleep for {interval} seconds")
        time.sleep(interval)


if __name__ == '__main__':
    main()
