import psycopg2

host = "localhost"
port = 8812
user = "admin"
password = "quest"
dbname = "qdb"

# (時刻, センサー名, 計測値) の時系列データ
readings = [
    ("2026-01-01T00:00:00.000000", "Alice", 10.0),
    ("2026-01-01T00:15:00.000000", "Alice", 12.0),
    ("2026-01-01T00:30:00.000000", "Alice", 11.0),
    ("2026-01-01T01:00:00.000000", "Alice", 20.0),
    ("2026-01-01T01:30:00.000000", "Alice", 22.0),
    ("2026-01-01T00:00:00.000000", "Bob", 5.0),
    ("2026-01-01T00:20:00.000000", "Bob", 7.0),
    ("2026-01-01T01:10:00.000000", "Bob", 9.0),
]


def connect():
    conn = psycopg2.connect(
        host=host, port=port, user=user, password=password, dbname=dbname
    )
    conn.autocommit = True
    return conn


def create_table():

    print("=== TIMESERIES TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("create table")

    cursor.execute("DROP TABLE IF EXISTS metrics;")
    cursor.execute("""
        CREATE TABLE metrics (
            ts     TIMESTAMP,
            sensor SYMBOL,
            value  DOUBLE
        ) TIMESTAMP(ts) PARTITION BY DAY;
    """)

    print("insert data")

    for t, sensor, value in readings:
        cursor.execute("INSERT INTO metrics VALUES (%s, %s, %s);", (t, sensor, value))

    for t, sensor, value in readings:
        print("Data row =", t, sensor, value)

    cursor.close()
    conn.close()


def sample_by_search():

    print("=== SAMPLE BY TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("aggregate Alice by 1 hour (SAMPLE BY)")

    # SAMPLE BY で 1 時間ごとにまとめ、平均値を計算する (QuestDB の時系列集計)
    cursor.execute(
        """
        SELECT ts, avg(value) AS avg_value, count() AS n
        FROM metrics
        WHERE sensor = %s
        SAMPLE BY 1h;
        """,
        ("Alice",),
    )
    for row in cursor.fetchall():
        print("Data row =", row[0], "avg =", round(row[1], 2), "n =", row[2])

    cursor.close()
    conn.close()


if __name__ == "__main__":

    create_table()

    sample_by_search()
