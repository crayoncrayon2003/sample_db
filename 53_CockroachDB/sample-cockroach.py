import psycopg2
from psycopg2.extras import Json

host = "localhost"
port = 26257
dbname = "test"
user = "root"
password = ""


def connect():
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        sslmode="disable"
    )


def sql():

    print("=== SQL TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("create table")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sql_table (
            id SERIAL PRIMARY KEY,
            name STRING,
            quantity INT
        );
    """)

    print("insert data")

    cursor.execute(
        "INSERT INTO sql_table (name, quantity) VALUES (%s,%s);",
        ("banana", 150)
    )

    cursor.execute(
        "INSERT INTO sql_table (name, quantity) VALUES (%s,%s);",
        ("orange", 154)
    )

    cursor.execute(
        "INSERT INTO sql_table (name, quantity) VALUES (%s,%s);",
        ("apple", 100)
    )

    conn.commit()

    print("select data")

    cursor.execute("SELECT * FROM sql_table;")

    rows = cursor.fetchall()

    for row in rows:
        print("Data row =", row)

    cursor.close()
    conn.close()


def nosql():

    print("=== JSON TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("create table")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nosql_table (
            id SERIAL PRIMARY KEY,
            name STRING,
            quantity INT,
            info JSONB
        );
    """)

    print("insert data")

    cursor.execute(
        "INSERT INTO nosql_table (name, quantity, info) VALUES (%s,%s,%s);",
        ("banana", 150, Json({"key1": 10, "key2": "update"}))
    )

    cursor.execute(
        "INSERT INTO nosql_table (name, quantity, info) VALUES (%s,%s,%s);",
        ("orange", 154, Json({"key1": 20, "key2": "update"}))
    )

    cursor.execute(
        "INSERT INTO nosql_table (name, quantity, info) VALUES (%s,%s,%s);",
        ("apple", 100, Json({"key1": 30, "key2": "update"}))
    )

    conn.commit()

    print("select data")

    cursor.execute("SELECT * FROM nosql_table;")

    rows = cursor.fetchall()

    for row in rows:
        print("Data row =", row)

    cursor.close()
    conn.close()


if __name__ == "__main__":

    sql()

    nosql()