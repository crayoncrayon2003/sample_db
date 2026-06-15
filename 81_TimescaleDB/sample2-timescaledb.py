import psycopg2

host = "localhost"
user = "user"
password = "user"

# (時刻, センサー名, 計測値) の時系列データ
readings = [
    ("2026-01-01 00:00:00", "Alice", 10.0),
    ("2026-01-01 00:15:00", "Alice", 12.0),
    ("2026-01-01 00:30:00", "Alice", 11.0),
    ("2026-01-01 01:00:00", "Alice", 20.0),
    ("2026-01-01 01:30:00", "Alice", 22.0),
    ("2026-01-01 00:00:00", "Bob", 5.0),
    ("2026-01-01 00:20:00", "Bob", 7.0),
    ("2026-01-01 01:10:00", "Bob", 9.0),
]


def connect():
    conn_string = "host={0} user={1} password={2}".format(host, user, password)
    conn = psycopg2.connect(conn_string)
    # timescaledb 拡張を有効化する
    conn.cursor().execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
    conn.commit()
    return conn


def create_hypertable():

    print("=== TIMESERIES TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("create hypertable")

    cursor.execute("DROP TABLE IF EXISTS metrics;")
    cursor.execute("""
        CREATE TABLE metrics (
            time   TIMESTAMPTZ NOT NULL,
            sensor TEXT,
            value  DOUBLE PRECISION
        );
    """)
    cursor.execute("SELECT create_hypertable('metrics', 'time');")
    conn.commit()

    print("insert data")

    for t, sensor, value in readings:
        cursor.execute(
            "INSERT INTO metrics (time, sensor, value) VALUES (%s, %s, %s);",
            (t, sensor, value),
        )
    conn.commit()

    for t, sensor, value in readings:
        print("Data row =", t, sensor, value)

    cursor.close()
    conn.close()


def bucket_search():

    print("=== TIME BUCKET TEST ===")

    conn = connect()
    cursor = conn.cursor()

    print("aggregate Alice by 1 hour bucket")

    # time_bucket で 1 時間ごとにまとめ、平均値を計算する (ダウンサンプリング)
    cursor.execute(
        """
        SELECT time_bucket('1 hour', time) AS bucket, sensor,
               avg(value) AS avg_value, count(*) AS n
        FROM metrics
        WHERE sensor = %s
        GROUP BY bucket, sensor
        ORDER BY bucket;
        """,
        ("Alice",),
    )
    for row in cursor.fetchall():
        print("Data row =", row[0], row[1], "avg =", round(row[2], 2), "n =", row[3])

    cursor.close()
    conn.close()


if __name__ == "__main__":

    create_hypertable()

    bucket_search()
