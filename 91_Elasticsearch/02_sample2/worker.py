import json
import redis
from elasticsearch import Elasticsearch

# === Queue パターン (consumer / worker) ===
# Redis の List (キュー) からイベントを取り出し、Elasticsearch へ反映する。
# アプリ (app.py) とは別プロセスで動き、ES が遅い/落ちていてもアプリを待たせない。

REDIS = dict(host="localhost", port=6379)
ES_HOST = "http://localhost:9200"
QUEUE_KEY = "products:changes"
INDEX = "products"


def setup_es(es):
    if not es.indices.exists(index=INDEX):
        es.indices.create(index=INDEX)


def main():
    r = redis.Redis(**REDIS)
    es = Elasticsearch(ES_HOST)

    setup_es(es)

    print("worker started. waiting for messages... (Ctrl-C to stop)")
    while True:
        # blpop はキューが空ならブロックして待つ (timeout=5 秒)
        item = r.blpop(QUEUE_KEY, timeout=5)
        if item is None:
            continue

        _, raw = item
        doc = json.loads(raw)

        es.index(
            index=INDEX,
            id=doc["id"],
            document={
                "name": doc["name"],
                "description": doc["description"],
                "quantity": doc["quantity"],
            },
        )
        es.indices.refresh(index=INDEX)
        print("indexed =", doc["id"], doc["name"])


if __name__ == "__main__":
    main()
