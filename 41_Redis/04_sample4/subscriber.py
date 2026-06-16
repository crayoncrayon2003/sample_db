import json

import redis

REDIS = dict(host="localhost", port=6384, decode_responses=True)
CHANNEL = "events:notifications"
MAX_MESSAGES = 3


def main():
    client = redis.Redis(**REDIS)
    pubsub = client.pubsub()
    pubsub.subscribe(CHANNEL)
    print("subscribed =", CHANNEL)

    received = 0
    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        event = json.loads(message["data"])
        received += 1
        print("received =", event)

        if received >= MAX_MESSAGES:
            break

    pubsub.close()


if __name__ == "__main__":
    main()
