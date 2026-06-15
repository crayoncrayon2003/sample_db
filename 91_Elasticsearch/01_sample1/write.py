import psycopg2
from elasticsearch import Elasticsearch

# === Dual Write パターン (書き込み) ===
# アプリが「正データ (PostgreSQL)」と「検索用 (Elasticsearch)」の両方に
# 自分で書き込む。同期の責任はアプリ側にある。
#
# 書き込んだ内容は read_postgres.py / read_elasticsearch.py でそれぞれ確認できる。

PG = dict(host="localhost", port=5432, dbname="test", user="user", password="user")
ES_HOST = "http://localhost:9200"
INDEX = "products"

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


def setup_es(es):
    if es.indices.exists(index=INDEX):
        es.indices.delete(index=INDEX)
    es.indices.create(index=INDEX)


def dual_write(conn, es, row):
    id_, name, description, quantity = row

    # ① 正データ (PostgreSQL) に書く
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (id, name, description, quantity) VALUES (%s, %s, %s, %s);",
        row,
    )
    conn.commit()
    cur.close()

    # ② 同じ内容を検索用 (Elasticsearch) にも書く  ← アプリが明示的に同期
    es.index(
        index=INDEX,
        id=id_,
        document={"name": name, "description": description, "quantity": quantity},
    )


def main():
    conn = psycopg2.connect(**PG)
    es = Elasticsearch(ES_HOST)

    print("setup postgres / elasticsearch")
    setup_postgres(conn)
    setup_es(es)

    print("dual write (PostgreSQL + Elasticsearch)")
    for row in products:
        dual_write(conn, es, row)
        print("write =", row[0], row[1])
    es.indices.refresh(index=INDEX)

    print("done. use read_postgres.py / read_elasticsearch.py to read it back")

    es.close()
    conn.close()


if __name__ == "__main__":
    main()
