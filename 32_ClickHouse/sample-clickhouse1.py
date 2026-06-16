import time

import clickhouse_connect

HOST = "localhost"
PORT = 8123
USER = "user"
PASSWORD = "user"
DATABASE = "sample_db"
TABLE = "sample_items"


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
    print("create table")
    client.command("DROP TABLE IF EXISTS {0}".format(TABLE))
    client.command(
        """
        CREATE TABLE {0} (
            id UInt32,
            name String,
            quantity UInt32
        )
        ENGINE = MergeTree
        ORDER BY id
        """.format(TABLE)
    )


def set_data(client):
    print("set data")
    rows = [
        [1, "banana", 150],
        [2, "orange", 154],
        [3, "apple", 100],
    ]
    client.insert(TABLE, rows, column_names=["id", "name", "quantity"])


def get_data(client):
    print("get data")
    rows = client.query("SELECT id, name, quantity FROM {0} ORDER BY id".format(TABLE))
    for row in rows.result_rows:
        print("Data row = (%s, %s, %s)" % (row[0], row[1], row[2]))


def main():
    client = connect_client()
    make_table(client)
    set_data(client)
    get_data(client)
    client.close()


if __name__ == "__main__":
    main()
