from pymongo import MongoClient

def main():
    # Connect to the server
    client = MongoClient("mongodb://localhost:27020")

    # Connect to the database. If the database does not exist, create it.
    db = client["testdb"]

    # Connect to the collection. If the collection does not exist, create it.
    collection = db["test_collection"]

    # insert
    collection.insert_one({"name": "TestA", "age": 100})

    # get
    for user in collection.find():
        print(user)

    client.close()

if __name__ == '__main__':
    main()