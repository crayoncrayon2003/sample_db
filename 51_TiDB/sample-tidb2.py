from time import sleep
import mysql.connector
import random
import datetime

MYHOST = '127.0.0.1'
MYPORT = 4000
MYUSER = 'root'
MYPASS = ''
MYDB   = 'sample_db'
MYTB   = 'my_table'


def connect_db(use_db=False):
    if use_db:
        return mysql.connector.connect(
            host=MYHOST, port=MYPORT, user=MYUSER, password=MYPASS, database=MYDB
        )
    else:
        return mysql.connector.connect(
            host=MYHOST, port=MYPORT, user=MYUSER, password=MYPASS
        )


def createDatabase():
    print("--- create database ---")
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYDB}")

    cursor.close()
    connect.close()


def deleteTable():
    print("--- delete Table ---")
    connect = connect_db(True)
    cursor = connect.cursor()

    try:
        sql = f"DROP TABLE IF EXISTS {MYTB}"
        cursor.execute(sql)
        connect.commit()
    except Exception as e:
        print("failure deleteTable", e)

    cursor.close()
    connect.close()


def makeTable():
    print("--- make Table ---")
    connect = connect_db(True)
    cursor = connect.cursor()

    try:
        sql = f'''
        CREATE TABLE {MYTB} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            device VARCHAR(40),
            temperature INT,
            humidity INT,
            battery INT,
            updateday DATETIME
        )
        '''
        cursor.execute(sql)
        connect.commit()

    except Exception as e:
        print("failure makeTable", e)

    cursor.close()
    connect.close()


def addTableData():
    print("--- add TableData ---")
    connect = connect_db(True)
    cursor = connect.cursor()

    temperature = 10
    humidity = 10
    battery = 10

    for i in range(5):
        try:
            for item in ["device1","device2","device3"]:
                dt = datetime.datetime.now()

                sql = f"""
                INSERT INTO {MYTB}
                (device, temperature, humidity, battery, updateday)
                VALUES (%s,%s,%s,%s,%s)
                """

                cursor.execute(
                    sql,
                    (item, temperature, humidity, battery, dt.isoformat())
                )

                connect.commit()

                print(
                    "device:",item,
                    "temperature:",temperature,
                    "humidity:",humidity,
                    "battery:",battery,
                    "time:",dt.isoformat()
                )

                temperature += random.randint(-3,3)
                humidity += random.randint(-3,3)
                battery += random.randint(-3,3)

            sleep(2)

        except Exception as e:
            print("failure addTableData", e)
            break

    cursor.close()
    connect.close()


def showTable():
    print("--- show Table ---")
    connect = connect_db(True)
    cursor = connect.cursor()

    cursor.execute(f"SELECT * FROM {MYTB}")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    connect.close()


if __name__ == "__main__":
    createDatabase()
    deleteTable()
    makeTable()
    addTableData()

    #showTable()