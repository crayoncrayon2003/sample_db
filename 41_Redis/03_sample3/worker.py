import json
import time

import redis

REDIS = dict(host="localhost", port=6383, decode_responses=True)
QUEUE_KEY = "tasks:queue"


def process_task(task):
    print("processing =", task)
    time.sleep(1)
    print("done =", task["id"])


def main():
    client = redis.Redis(**REDIS)
    print("waiting for tasks")

    while True:
        item = client.blpop(QUEUE_KEY, timeout=10)
        if item is None:
            print("no task")
            break

        _, payload = item
        task = json.loads(payload)
        process_task(task)


if __name__ == "__main__":
    main()
