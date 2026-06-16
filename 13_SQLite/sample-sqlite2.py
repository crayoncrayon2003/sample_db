import datetime
import random
import sqlite3

DB_PATH = "sample.db"
MYTB = "sensor_table"


def connect_db():
    return sqlite3.connect(DB_PATH)


def delete_table():
    print("--- delete Table ---")
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute("DROP TABLE IF EXISTS {0}".format(MYTB))
    connect.commit()

    cursor.close()
    connect.close()


def make_table():
    print("--- make Table ---")
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        """
        CREATE TABLE {0} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT NOT NULL,
            temperature INTEGER,
            humidity INTEGER,
            battery INTEGER,
            updateday TEXT
        )
        """.format(MYTB)
    )
    connect.commit()

    cursor.execute("PRAGMA table_info({0});".format(MYTB))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    connect.close()


def add_table_data():
    print("--- add TableData ---")
    connect = connect_db()
    cursor = connect.cursor()

    temperature = 10
    humidity = 10
    battery = 10

    for _ in range(5):
        for item in ["device1", "device2", "device3"]:
            dt = datetime.datetime.now()

            cursor.execute(
                """
                INSERT INTO {0}
                (device, temperature, humidity, battery, updateday)
                VALUES (?, ?, ?, ?, ?)
                """.format(MYTB),
                (item, temperature, humidity, battery, dt.isoformat()),
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
                dt.isoformat(),
            )

            temperature += random.randint(-3, 3)
            humidity += random.randint(-3, 3)
            battery += random.randint(-3, 3)

    connect.commit()
    cursor.close()
    connect.close()


def show_table():
    print("--- show Table ---")
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM {0} ORDER BY id;".format(MYTB))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    connect.close()


if __name__ == "__main__":
    delete_table()
    make_table()
    add_table_data()
    show_table()
