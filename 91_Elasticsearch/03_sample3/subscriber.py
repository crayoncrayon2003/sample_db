import json
import redis
from elasticsearch import Elasticsearch

# === CDC パターン (subscriber) ===
# Debezium が Redis Streams に流した変更イベントを subscribe し、
# Elasticsearch へ反映する。Debezium がブローカーへ publish する仕組みなので、
# 自前で WAL を読むサーバを書く必要はない (consumer group で購読するだけ)。

REDIS = dict(host="localhost", port=6379)
ES_HOST = "http://localhost:9200"
STREAM = "cdc.public.products"  # topic.prefix + schema + table
GROUP = "es-indexer"
CONSUMER = "consumer-1"
INDEX = "products"


def setup_es(es):
    if not es.indices.exists(index=INDEX):
        es.indices.create(index=INDEX)


def ensure_group(r):
    try:
        # ストリームがまだ無くても mkstream で作成しつつ consumer group を作る
        r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
    except redis.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise


def extract_event(fields):
    # Debezium の Redis sink は {keyJson: valueJson} の形で書き込むため、
    # 変更イベント (op / after / before を持つ JSON) を取り出す。
    for raw in list(fields.values()) + list(fields.keys()):
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if isinstance(obj, dict) and ("op" in obj or "after" in obj):
            return obj
    return None


def apply_event(es, event):
    op = event.get("op")
    after = event.get("after")
    before = event.get("before")

    if op in ("c", "r", "u") and after:
        es.index(
            index=INDEX,
            id=after["id"],
            document={
                "name": after["name"],
                "description": after["description"],
                "quantity": after["quantity"],
            },
        )
        print("indexed =", op, after["id"], after["name"])
    elif op == "d" and before:
        es.delete(index=INDEX, id=before["id"], ignore=[404])
        print("deleted =", before["id"])


def main():
    r = redis.Redis(**REDIS)
    es = Elasticsearch(ES_HOST)
    setup_es(es)
    ensure_group(r)

    print("subscriber started. waiting for CDC events... (Ctrl-C to stop)")
    while True:
        resp = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=5000)
        if not resp:
            continue
        for _stream, entries in resp:
            for entry_id, fields in entries:
                event = extract_event(fields)
                if event:
                    apply_event(es, event)
                r.xack(STREAM, GROUP, entry_id)
        es.indices.refresh(index=INDEX)


if __name__ == "__main__":
    main()
