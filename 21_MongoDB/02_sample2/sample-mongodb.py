from pymongo import MongoClient
from time import sleep
import random
import datetime

def main():
    uri = "mongodb://localhost:27017/?replicaSet=dbrs"

    # Connect to the server
    client = MongoClient(uri)

    # Connect to the database. If the database does not exist, create it.
    db = client["testdb"]

    # Connect to the collection. If the collection does not exist, create it.
    collection = db["test_collection"]

    # insert
    temperature = 10
    humidity = 10
    battery = 10

    dt = datetime.datetime.now()
    dt = dt + datetime.timedelta(days=-2)

    try:
        for i in range(10):
            for item in ['device1', 'device2', 'device3']:
                data = {
                    'device': item,
                    'temperature': temperature,
                    'humidity': humidity,
                    'battery': battery,
                    'updateday': dt
                }

                collection.insert_one(data)

                print(
                    "device:", item,
                    "temperature:", temperature,
                    "humidity:", humidity,
                    "battery:", battery,
                    "time:", dt
                )

                temperature += random.randint(-3, 3)
                humidity += random.randint(-3, 3)
                battery += random.randint(-3, 3)

                dt = dt + datetime.timedelta(milliseconds=5)

            dt = dt + datetime.timedelta(milliseconds=30)
            sleep(3)

    except Exception as e:
        print("データ登録失敗:", e)

    # get
    print("--- stored documents ---")

    for user in collection.find():
        print(user)

    client.close()


if __name__ == '__main__':
    main()