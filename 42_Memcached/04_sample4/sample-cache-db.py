import json
import time

import psycopg2
from pymemcache.client.base import Client

PG = dict(host="localhost", port=5434, dbname="sample_db", user="user", password="user")
MEMCACHED = ("localhost", 11215)

products = [
    (1, "Apple MacBook", "lightweight laptop", 10),
    (2, "Banana Phone", "yellow smartphone", 25),
    (3, "Orange Tablet", "tablet for reading", 15),
]


def connect_postgres():
    for _ in range(30):
        try:
            return psycopg2.connect(**PG)
        except psycopg2.OperationalError:
            time.sleep(2)

    raise RuntimeError("Could not connect to PostgreSQL")


def setup_postgres(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products;")
    cur.execute(
        """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            description TEXT,
            quantity INTEGER
        );
        """
    )
    cur.executemany(
        "INSERT INTO products (id, name, description, quantity) VALUES (%s, %s, %s, %s);",
        products,
    )
    conn.commit()
    cur.close()


def get_product_from_db(conn, product_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, description, quantity FROM products WHERE id = %s;",
        (product_id,),
    )
    row = cur.fetchone()
    cur.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "quantity": row[3],
    }


def get_product(conn, cache, product_id):
    key = "product:{0}".format(product_id)
    cached = cache.get(key)
    if cached is not None:
        return "memcached", json.loads(cached.decode("utf-8"))

    product = get_product_from_db(conn, product_id)
    if product is None:
        return "not_found", None

    cache.set(key, json.dumps(product).encode("utf-8"), expire=60)
    return "postgres", product


def main():
    conn = connect_postgres()
    cache = Client(MEMCACHED, connect_timeout=3, timeout=3)

    try:
        setup_postgres(conn)
        cache.flush_all()

        for index in range(1, 4):
            source, product = get_product(conn, cache, 1)
            print("request =", index, "source =", source, "product =", product)
    finally:
        cache.close()
        conn.close()


if __name__ == "__main__":
    main()
