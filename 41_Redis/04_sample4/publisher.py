import json
import time

import redis

REDIS = dict(host="localhost", port=6384, decode_responses=True)
CHANNEL = "events:notifications"

events = [
    {"event": "user.created", "user": "alice"},
    {"event": "order.created", "order_id": "order-001"},
    {"event": "inventory.updated", "sku": "sku-001", "quantity": 42},
]


def main():
    client = redis.Redis(**REDIS)

    for event in events:
        client.publish(CHANNEL, json.dumps(event))
        print("published =", event)
        time.sleep(1)


if __name__ == "__main__":
    main()
