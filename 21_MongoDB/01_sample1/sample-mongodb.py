from pymongo import MongoClient
from time import sleep
import random
import datetime

def main():
    # Connect to the server
    client = MongoClient("mongodb://localhost:27017")

    # Connect to the database. If the database does not exist, create it.
    db = client["testdb"]

    # Connect to the collection. If the collection does not exist, create it.
    collection = db["test_collection"]

    # insert
    temperature = 10
    humidity = 10
    battery  = 10
    dt = datetime.datetime.now()
    dt = dt+datetime.timedelta(days=-2)
    try :
        for i in range(10):
            for item in ['device1','device2','device3']:
                data = {
                    'device':item,
                    'temperature':temperature,
                    'humidity':humidity,
                    'battery':battery,
                    'updateday':dt.strftime('%Y-%m-%d %H:%M:%S.%f')
                }
                collection.insert_one(data)
                print("device:",item,"temperature:",temperature, "humidity:",humidity, "battery:",battery, "time:",dt.strftime('%Y-%m-%d %H:%M:%S.%f'))
                temperature += random.randint(-3, 3)
                humidity += random.randint(-3, 3)
                battery += random.randint(-3, 3)
                dt = dt + datetime.timedelta(milliseconds=5)

            dt = dt + datetime.timedelta(milliseconds=30)
            sleep(3)
    except:
        print("データ登録失敗")
    finally:
        client.close()

    # get
    for user in collection.find():
        print(user)

    client.close()

if __name__ == '__main__':
    main()