import psycopg2
from pgvector.psycopg2 import register_vector

host = "localhost"
user = "user"
password = "user"
vector_size = 4

# 各人物を 4 次元の特徴ベクトルで表す
people = [
    {"id": 1, "name": "Alice", "vector": [0.1, 0.9, 0.3, 0.0]},
    {"id": 2, "name": "Bob", "vector": [0.2, 0.8, 0.2, 0.1]},
    {"id": 3, "name": "Carol", "vector": [0.9, 0.1, 0.8, 0.2]},
    {"id": 4, "name": "Dave", "vector": [0.8, 0.2, 0.9, 0.1]},
    {"id": 5, "name": "Eve", "vector": [0.3, 0.7, 0.0, 0.9]},
]


def connect():
    conn_string = "host={0} user={1} password={2}".format(host, user, password)
    conn = psycopg2.connect(conn_string)
    # vector 拡張を有効化してから型を登録する
    conn.cursor().execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()
    register_vector(conn)
    return conn


def create_table():

    print("=== PERSON VECTOR TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("create table")

    cursor.execute("DROP TABLE IF EXISTS person_table;")
    cursor.execute("""
        CREATE TABLE person_table (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50),
            embedding vector(%s)
        );
    """ % vector_size)

    print("insert data")

    for p in people:
        cursor.execute(
            "INSERT INTO person_table (id, name, embedding) VALUES (%s, %s, %s);",
            (p["id"], p["name"], p["vector"]),
        )
    conn.commit()

    for p in people:
        print("Data row =", p["id"], p["name"])

    cursor.close()
    conn.close()


def similar_search():

    print("=== SIMILAR PERSON SEARCH TEST ===")

    conn = connect()
    cursor = conn.cursor()

    target = "Alice"

    print("search people similar to", target)

    # 基準人物のベクトルを副問い合わせで取り出し、<=> (コサイン距離) が
    # 小さい順 = 似ている順に並べる。自分自身は WHERE で除外する
    cursor.execute(
        """
        SELECT id, name,
               embedding <=> (SELECT embedding FROM person_table WHERE name = %s) AS distance
        FROM person_table
        WHERE name <> %s
        ORDER BY distance
        LIMIT 3;
        """,
        (target, target),
    )

    for row in cursor.fetchall():
        print("Data row =", row[0], row[2], {"name": row[1]})

    cursor.close()
    conn.close()


if __name__ == "__main__":

    create_table()

    similar_search()
