import json

import redis

REDIS = dict(host="localhost", port=6383, decode_responses=True)
QUEUE_KEY = "tasks:queue"

tasks = [
    {"id": 1, "type": "resize-image", "target": "image-001.png"},
    {"id": 2, "type": "send-mail", "target": "user@example.com"},
    {"id": 3, "type": "create-report", "target": "sales-2026-06"},
]


def main():
    client = redis.Redis(**REDIS)
    client.delete(QUEUE_KEY)

    print("push tasks")
    for task in tasks:
        client.rpush(QUEUE_KEY, json.dumps(task))
        print("queued =", task)

    print("queue length =", client.llen(QUEUE_KEY))


if __name__ == "__main__":
    main()
