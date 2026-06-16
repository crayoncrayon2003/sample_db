import datetime
import random
import time

from cassandra.cluster import Cluster
from cassandra.cluster import NoHostAvailable

HOST = "127.0.0.1"
PORT = 9042
KEYSPACE = "sample_keyspace"
TABLE = "sample_sensors"


def connect_session():
    cluster = Cluster([HOST], port=PORT)

    for _ in range(30):
        try:
            session = cluster.connect()
            return cluster, session
        except NoHostAvailable:
            time.sleep(2)

    cluster.shutdown()
    raise RuntimeError("Could not connect to ScyllaDB")


def prepare_keyspace(session):
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS sample_keyspace
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """
    )
    session.set_keyspace(KEYSPACE)


def make_table(session):
    print("--- make Table ---")
    session.execute("DROP TABLE IF EXISTS {0};".format(TABLE))
    session.execute(
        """
        CREATE TABLE {0} (
            device text,
            updateday timestamp,
            temperature int,
            humidity int,
            battery int,
            PRIMARY KEY (device, updateday)
        ) WITH CLUSTERING ORDER BY (updateday ASC)
        """.format(TABLE)
    )


def add_table_data(session):
    print("--- add TableData ---")

    temperature = 10
    humidity = 10
    battery = 10
    dt = datetime.datetime.now() + datetime.timedelta(days=-2)

    for _ in range(5):
        for item in ["device1", "device2", "device3"]:
            session.execute(
                """
                INSERT INTO {0}
                (device, updateday, temperature, humidity, battery)
                VALUES (%s, %s, %s, %s, %s)
                """.format(TABLE),
                (item, dt, temperature, humidity, battery),
            )

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


def query_table(session):
    print("--- query Table ---")
    rows = session.execute(
        """
        SELECT device, updateday, temperature, humidity, battery
        FROM {0}
        WHERE device = %s
        """.format(TABLE),
        ("device1",),
    )

    for row in rows:
        print(
            "Data row = (%s, %s, %s, %s, %s)"
            % (
                row.device,
                row.updateday.strftime("%Y-%m-%d %H:%M:%S.%f"),
                row.temperature,
                row.humidity,
                row.battery,
            )
        )


def main():
    cluster, session = connect_session()
    try:
        prepare_keyspace(session)
        make_table(session)
        add_table_data(session)
        query_table(session)
    finally:
        cluster.shutdown()


if __name__ == "__main__":
    main()
