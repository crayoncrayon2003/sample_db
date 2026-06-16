import datetime
import random

import mysql.connector

MYHOST = "127.0.0.1"
MYPORT = 3307
MYUSER = "user"
MYPASS = "user"
MYDB = "sample_db"
MYTB = "sensor_table"


def connect_db():
    return mysql.connector.connect(
        host=MYHOST,
        port=MYPORT,
        user=MYUSER,
        password=MYPASS,
        database=MYDB,
    )


def delete_table():
    print("--- delete Table ---")
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute("DROP TABLE IF EXISTS {0}".format(MYTB))
    connect.commit()

    cursor.close()
    connect.close()


def show_table():
    print("--- show Table ---")
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute("SHOW TABLES")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    connect.close()


def make_table():
    print("--- make Table ---")
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(
        """
        CREATE TABLE {0} (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            device VARCHAR(40),
            temperature INT,
            humidity INT,
            battery INT,
            updateday DATETIME
        )
        """.format(MYTB)
    )
    connect.commit()

    cursor.execute("SHOW COLUMNS FROM {0}".format(MYTB))
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
                VALUES (%s, %s, %s, %s, %s)
                """.format(MYTB),
                (item, temperature, humidity, battery, dt.strftime("%Y-%m-%d %H:%M:%S")),
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


if __name__ == "__main__":
    delete_table()
    make_table()
    add_table_data()
    show_table()
