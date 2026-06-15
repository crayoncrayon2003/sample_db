import psycopg2
from pgvector.psycopg2 import register_vector

host = "localhost"
user = "user"
password = "user"
vector_size = 4


def connect():
    conn_string = "host={0} user={1} password={2}".format(host, user, password)
    conn = psycopg2.connect(conn_string)
    # vector 拡張を有効化してから型を登録する
    conn.cursor().execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()
    register_vector(conn)
    return conn


def vector_search():

    print("=== VECTOR TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("create table")

    cursor.execute("DROP TABLE IF EXISTS vector_table;")
    cursor.execute("""
        CREATE TABLE vector_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            quantity INTEGER,
            embedding vector(%s)
        );
    """ % vector_size)

    print("insert data")

    cursor.execute(
        "INSERT INTO vector_table (name, quantity, embedding) VALUES (%s, %s, %s);",
        ("banana", 150, [0.10, 0.20, 0.30, 0.40])
    )
    cursor.execute(
        "INSERT INTO vector_table (name, quantity, embedding) VALUES (%s, %s, %s);",
        ("orange", 154, [0.20, 0.10, 0.40, 0.30])
    )
    cursor.execute(
        "INSERT INTO vector_table (name, quantity, embedding) VALUES (%s, %s, %s);",
        ("apple", 100, [0.90, 0.80, 0.70, 0.60])
    )
    conn.commit()

    print("search data")

    # <=> はコサイン距離 (小さいほど類似)。クエリベクトルは ::vector で明示キャストする
    cursor.execute(
        """
        SELECT id, name, quantity, embedding <=> %s::vector AS distance
        FROM vector_table
        ORDER BY distance
        LIMIT 3;
        """,
        (str([0.15, 0.15, 0.35, 0.35]),)
    )

    for row in cursor.fetchall():
        print("Data row =", row[0], row[3], {"name": row[1], "quantity": row[2]})

    cursor.close()
    conn.close()


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("search data with filter (name = apple)")

    cursor.execute(
        """
        SELECT id, name, quantity, embedding <=> %s::vector AS distance
        FROM vector_table
        WHERE name = %s
        ORDER BY distance
        LIMIT 3;
        """,
        (str([0.15, 0.15, 0.35, 0.35]), "apple")
    )

    for row in cursor.fetchall():
        print("Data row =", row[0], row[3], {"name": row[1], "quantity": row[2]})

    cursor.close()
    conn.close()


if __name__ == "__main__":

    vector_search()

    filtered_search()
