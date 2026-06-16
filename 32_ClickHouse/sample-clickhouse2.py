import datetime
import random
import time

import clickhouse_connect

HOST = "localhost"
PORT = 8123
USER = "user"
PASSWORD = "user"
DATABASE = "sample_db"
TABLE = "sample_sensors"


def connect_client():
    for _ in range(30):
        try:
            return clickhouse_connect.get_client(
                host=HOST,
                port=PORT,
                username=USER,
                password=PASSWORD,
                database=DATABASE,
            )
        except Exception:
            time.sleep(2)

    raise RuntimeError("Could not connect to ClickHouse")


def make_table(client):
    print("--- make Table ---")
    client.command("DROP TABLE IF EXISTS {0}".format(TABLE))
    client.command(
        """
        CREATE TABLE {0} (
            device String,
            temperature Int32,
            humidity Int32,
            battery Int32,
            updateday DateTime64(3)
        )
        ENGINE = MergeTree
        ORDER BY (device, updateday)
        """.format(TABLE)
    )


def add_table_data(client):
    print("--- add TableData ---")

    rows = []
    temperature = 10
    humidity = 10
    battery = 10
    dt = datetime.datetime.now() + datetime.timedelta(days=-2)

    for _ in range(20):
        for item in ["device1", "device2", "device3"]:
            rows.append([item, temperature, humidity, battery, dt])
            print(
                "device:",
                item,
                "temperature:",
                temperature,
                "humidity:",
                humidity,
                "battery:",
                battery,
                "time:",
                dt.strftime("%Y-%m-%d %H:%M:%S.%f"),
            )

            temperature += random.randint(-3, 3)
            humidity += random.randint(-3, 3)
            battery += random.randint(-3, 3)
            dt = dt + datetime.timedelta(milliseconds=5)

        dt = dt + datetime.timedelta(milliseconds=30)

    client.insert(
        TABLE,
        rows,
        column_names=["device", "temperature", "humidity", "battery", "updateday"],
    )


def query_table(client):
    print("--- query Table ---")
    rows = client.query(
        """
        SELECT
            device,
            count() AS records,
            round(avg(temperature), 2) AS avg_temperature,
            min(battery) AS min_battery,
            max(updateday) AS latest_time
        FROM {0}
        GROUP BY device
        ORDER BY device
        """.format(TABLE)
    )

    for row in rows.result_rows:
        print(
            "Data row = (%s, %s, %s, %s, %s)"
            % (row[0], row[1], row[2], row[3], row[4])
        )


def main():
    client = connect_client()
    make_table(client)
    add_table_data(client)
    query_table(client)
    client.close()


if __name__ == "__main__":
    main()
