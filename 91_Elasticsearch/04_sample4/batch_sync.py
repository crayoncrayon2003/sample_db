import os
import psycopg2
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# === Batch パターン (定期同期) ===
# 前回の同期時刻 (watermark) より後に更新された行だけを PostgreSQL から
# SELECT し、Elasticsearch へまとめて (bulk) 反映する。
# このスクリプトを cron などで定期実行すると差分同期になる。

PG = dict(host="localhost", port=5432, dbname="test", user="user", password="user")
ES_HOST = "http://localhost:9200"
INDEX = "products"
WATERMARK_FILE = ".watermark"
EPOCH = "1970-01-01 00:00:00"


def load_watermark():
    if os.path.exists(WATERMARK_FILE):
        with open(WATERMARK_FILE) as f:
            return f.read().strip()
    return EPOCH


def save_watermark(value):
    with open(WATERMARK_FILE, "w") as f:
        f.write(value)


def setup_es(es):
    if not es.indices.exists(index=INDEX):
        es.indices.create(index=INDEX)


def main():
    conn = psycopg2.connect(**PG)
    es = Elasticsearch(ES_HOST)
    setup_es(es)

    watermark = load_watermark()
    print("sync rows updated after:", watermark)

    cur = conn.cursor()
    # watermark より後に更新された行だけ取得する (差分同期)
    cur.execute(
        """
        SELECT id, name, description, quantity, updated_at
        FROM products
        WHERE updated_at > %s
        ORDER BY updated_at;
        """,
        (watermark,),
    )
    rows = cur.fetchall()

    if not rows:
        print("no changes.")
        cur.close()
        conn.close()
        es.close()
        return

    actions = []
    max_updated = watermark
    for id_, name, description, quantity, updated_at in rows:
        actions.append({
            "_index": INDEX,
            "_id": id_,
            "_source": {"name": name, "description": description, "quantity": quantity},
        })
        ts = updated_at.strftime("%Y-%m-%d %H:%M:%S.%f")
        if ts > max_updated:
            max_updated = ts
        print("sync =", id_, name, "(updated_at:", ts, ")")

    bulk(es, actions)
    es.indices.refresh(index=INDEX)

    # 次回はこの時刻より後だけを対象にする
    save_watermark(max_updated)
    print("synced", len(actions), "rows. new watermark:", max_updated)

    cur.close()
    conn.close()
    es.close()


if __name__ == "__main__":
    main()
