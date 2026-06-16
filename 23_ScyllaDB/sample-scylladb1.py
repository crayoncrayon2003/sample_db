import time

from cassandra.cluster import Cluster
from cassandra.cluster import NoHostAvailable

HOST = "127.0.0.1"
PORT = 9042
KEYSPACE = "sample_keyspace"
TABLE = "sample_items"


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
    print("create table")
    session.execute("DROP TABLE IF EXISTS {0};".format(TABLE))
    session.execute(
        """
        CREATE TABLE {0} (
            id text PRIMARY KEY,
            name text,
            quantity int
        )
        """.format(TABLE)
    )


def set_data(session):
    print("set data")
    rows = [
        ("item-001", "banana", 150),
        ("item-002", "orange", 154),
        ("item-003", "apple", 100),
    ]

    for row in rows:
        session.execute(
            "INSERT INTO {0} (id, name, quantity) VALUES (%s, %s, %s);".format(TABLE),
            row,
        )


def get_data(session):
    print("get data")
    rows = session.execute("SELECT id, name, quantity FROM {0};".format(TABLE))
    for row in sorted(rows, key=lambda item: item.id):
        print("Data row = (%s, %s, %s)" % (row.id, row.name, row.quantity))


def main():
    cluster, session = connect_session()
    try:
        prepare_keyspace(session)
        make_table(session)
        set_data(session)
        get_data(session)
    finally:
        cluster.shutdown()


if __name__ == "__main__":
    main()
