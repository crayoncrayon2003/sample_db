import json
import psycopg2
import redis

# === Queue パターン (producer) ===
# アプリは「正データ (PostgreSQL)」に書いたあと、変更イベントを Redis の
# List (キュー) に push する。ES への反映はワーカー (worker.py) が担当する。
# 同期のきっかけを作るのはアプリだが、タイミングはワーカー側に分離される。

PG = dict(host="localhost", port=5432, dbname="test", user="user", password="user")
REDIS = dict(host="localhost", port=6379)
QUEUE_KEY = "products:changes"

# (id, name, description, quantity)
products = [
    (1, "Apple MacBook", "lightweight aluminum laptop with long battery life", 10),
    (2, "Banana Phone", "yellow curved smartphone with a retro design", 25),
    (3, "Orange Tablet", "vivid display tablet for reading and drawing", 15),
]


def setup_postgres(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products;")
    cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            description TEXT,
            quantity INTEGER
        );
    """)
    conn.commit()
    cur.close()


def write_and_enqueue(conn, r, row):
    id_, name, description, quantity = row
    doc = {"id": id_, "name": name, "description": description, "quantity": quantity}

    # ① 正データ (PostgreSQL) に書く
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (id, name, description, quantity) VALUES (%s, %s, %s, %s);",
        row,
    )
    conn.commit()
    cur.close()

    # ② 変更イベントをキューに push する  ← アプリが明示的に通知 (ES には触れない)
    r.rpush(QUEUE_KEY, json.dumps(doc))


def main():
    conn = psycopg2.connect(**PG)
    r = redis.Redis(**REDIS)

    print("setup postgres")
    setup_postgres(conn)

    print("write to PostgreSQL and enqueue changes to Redis")
    for row in products:
        write_and_enqueue(conn, r, row)
        print("enqueue =", row[0], row[1])

    print("queue length =", r.llen(QUEUE_KEY))
    print("-> run worker.py to consume the queue and index into Elasticsearch")

    conn.close()


if __name__ == "__main__":
    main()
