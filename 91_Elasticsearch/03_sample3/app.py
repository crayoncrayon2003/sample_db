import psycopg2

# === CDC パターン (アプリ) ===
# アプリは「正データ (PostgreSQL)」に書き込むだけ。
# Elasticsearch も Redis も一切知らない。同期コードは存在しない。
# 変更は Debezium が WAL から自動で拾い、Redis Streams に流す。

PG = dict(host="localhost", port=5432, dbname="test", user="user", password="user")

# (id, name, description, quantity)
products = [
    (1, "Apple MacBook", "lightweight aluminum laptop with long battery life", 10),
    (2, "Banana Phone", "yellow curved smartphone with a retro design", 25),
    (3, "Orange Tablet", "vivid display tablet for reading and drawing", 15),
]


def main():
    conn = psycopg2.connect(**PG)
    cur = conn.cursor()

    print("setup postgres")
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

    print("write to PostgreSQL only (no ES / Redis code here)")
    for row in products:
        cur.execute(
            "INSERT INTO products (id, name, description, quantity) VALUES (%s, %s, %s, %s);",
            row,
        )
        conn.commit()
        print("write =", row[0], row[1])

    cur.close()
    conn.close()
    print("-> Debezium will capture these changes from the WAL automatically")


if __name__ == "__main__":
    main()
