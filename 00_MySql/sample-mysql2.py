from time import sleep
import MySQLdb
import random
import datetime

MYHOST = '127.0.0.1'
MYPORT = 3306
MYUSER = 'user'
MYPASS = 'user'
MYDB   = 'sample_db'
MYTB   = 'my_table'

def deleteTable():
    print("--- delete Table ---")
    connect = MySQLdb.connect(host=MYHOST, port=MYPORT, user=MYUSER, passwd=MYPASS, db=MYDB)
    cursor = connect.cursor()

    try :
        sql = "DROP TABLE {0}".format(MYTB)
        cursor.execute(sql)
        connect.commit()
    except:
        print("failure deleteTable")

    cursor.close()
    connect.close()

def showTable():
    print("--- show Table ---")
    connect = MySQLdb.connect(host=MYHOST, port=MYPORT, user=MYUSER, passwd=MYPASS, db=MYDB)
    cursor = connect.cursor()

    try :
        cursor.execute("SHOW TABLES")
        print(cursor.fetchall())

        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except:
        print("failure showTable")

    cursor.close()
    connect.close()

def makeTable():
    print("--- make Table ---")
    connect = MySQLdb.connect(host=MYHOST, port=MYPORT, user=MYUSER, passwd=MYPASS, db=MYDB)
    cursor = connect.cursor()

    try :
        sql = '''CREATE TABLE {0} (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            device VARCHAR(40),
            temperature INT,
            humidity INT,
            battery INT,
            updateday DATETIME
            )
            '''.format(MYTB)

        cursor.execute(sql)
        connect.commit()

        sql = "show columns from {0}".format(MYTB)
        cursor.execute(sql)
    except:
        print("failure makeTable")

    cursor.close()
    connect.close()

def initTableData():
    print("--- init TableData ---")
    connect = MySQLdb.connect(host=MYHOST, port=MYPORT, user=MYUSER, passwd=MYPASS, db=MYDB)
    cursor = connect.cursor()

    temperature = 10
    humidity = 10
    battery  = 10
    dt = datetime.datetime.now()
    dt = dt+datetime.timedelta(days=-2)

    for i in range(100):
        try :
            for item in ["device1","device2","device3"]:
                sql = "INSERT INTO {0} (device, temperature, humidity, battery, updateday) VALUES (%s, %s, %s, %s, %s)".format(MYTB)
                cursor.execute(sql, (item, temperature, humidity, battery, dt.strftime('%Y-%m-%d %H:%M:%S.%f')))
                print("device:",item,"temperature:",temperature, "humidity:",humidity, "battery:",battery, "time:",dt.strftime('%Y-%m-%d %H:%M:%S.%f'))
                connect.commit()

                temperature += random.randint(-3, 3)
                humidity += random.randint(-3, 3)
                battery += random.randint(-3, 3)
                dt = dt + datetime.timedelta(milliseconds=5)

            dt = dt + datetime.timedelta(milliseconds=30)
            sleep(2)
        except:
            print("failure initTableData")
            break

    cursor.close()
    connect.close()


def addTableData():
    print("--- add TableData ---")
    connect = MySQLdb.connect(host=MYHOST, port=MYPORT, user=MYUSER, passwd=MYPASS, db=MYDB)
    cursor = connect.cursor()

    temperature = 10
    humidity = 10
    battery  = 10

    for i in range(5):
        try :
            for item in ["device1","device2","device3"]:
                dt = datetime.datetime.now()
                sql = "INSERT INTO {0} (device, temperature, humidity, battery, updateday) VALUES (%s, %s, %s, %s, %s)".format(MYTB)
                cursor.execute(sql, (item, temperature, humidity, battery, dt.isoformat()))
                print("device:",item,"temperature:",temperature, "humidity:",humidity, "battery:",battery, "time:",dt.isoformat())
                connect.commit()

                temperature += random.randint(-3, 3)
                humidity += random.randint(-3, 3)
                battery += random.randint(-3, 3)

            sleep(2)
        except:
            print("failure addTableData")
            break

    cursor.close()
    connect.close()


if __name__ == "__main__":
    deleteTable()
    makeTable()
    addTableData()

    #showTable()