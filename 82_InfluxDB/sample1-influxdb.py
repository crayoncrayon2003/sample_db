from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

url = "http://localhost:8086"
token = "sample-token"
org = "sample-org"
bucket = "sample-bucket"

# (時刻, センサー名, 計測値) の時系列データ
readings = [
    ("2026-01-01T00:00:00Z", "Alice", 10.0),
    ("2026-01-01T00:15:00Z", "Alice", 12.0),
    ("2026-01-01T00:30:00Z", "Alice", 11.0),
    ("2026-01-01T01:00:00Z", "Alice", 20.0),
    ("2026-01-01T01:30:00Z", "Alice", 22.0),
    ("2026-01-01T00:00:00Z", "Bob", 5.0),
    ("2026-01-01T00:20:00Z", "Bob", 7.0),
    ("2026-01-01T01:10:00Z", "Bob", 9.0),
]


def connect():
    return InfluxDBClient(url=url, token=token, org=org)


def write_points(client):
    # 既存の metrics データを削除してから書き込む
    client.delete_api().delete(
        "1970-01-01T00:00:00Z", "2100-01-01T00:00:00Z",
        '_measurement="metrics"', bucket=bucket, org=org,
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)
    points = [
        Point("metrics").tag("sensor", sensor).field("value", value).time(t)
        for t, sensor, value in readings
    ]
    write_api.write(bucket=bucket, org=org, record=points)


def timeseries_test():

    print("=== TIMESERIES TEST ===")

    client = connect()

    print("write data")

    write_points(client)

    print("query data")

    # range で時間範囲を絞り、time 順に取得する
    query = """
    from(bucket: "{bucket}")
      |> range(start: 2025-12-31T00:00:00Z, stop: 2026-01-02T00:00:00Z)
      |> filter(fn: (r) => r._measurement == "metrics")
      |> sort(columns: ["_time"])
    """.format(bucket=bucket)

    for table in client.query_api().query(query, org=org):
        for record in table.records:
            print("Data row =", record.get_time(), record.values.get("sensor"), record.get_value())

    client.close()


def filtered_query():

    print("=== FILTERED QUERY TEST ===")

    client = connect()

    print("query data with filter (sensor = Alice)")

    query = """
    from(bucket: "{bucket}")
      |> range(start: 2025-12-31T00:00:00Z, stop: 2026-01-02T00:00:00Z)
      |> filter(fn: (r) => r._measurement == "metrics")
      |> filter(fn: (r) => r.sensor == "Alice")
      |> sort(columns: ["_time"])
    """.format(bucket=bucket)

    for table in client.query_api().query(query, org=org):
        for record in table.records:
            print("Data row =", record.get_time(), record.values.get("sensor"), record.get_value())

    client.close()


if __name__ == "__main__":

    timeseries_test()

    filtered_query()
