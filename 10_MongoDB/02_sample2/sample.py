from pymongo import MongoClient, ReadPreference

def main():
    # Connect to the server
    #client = MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/',replicaSet="rs0", read_preference=ReadPreference.PRIMARY)
    client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019/',replicaSet="dbrs", read_preference=ReadPreference.PRIMARY)
    # client = MongoClient('mongodb://192.168.2.2:27017,192.168.2.3:27018,192.168.2.4:27019',replicaSet="dbrs", read_preference=ReadPreference.PRIMARY)
    # client = MongoClient('mongodb://0.0.0.0:27017,0.0.0.0:27018,0.0.0.0:27019',replicaSet="dbrs", read_preference=ReadPreference.PRIMARY)
    # client = MongoClient('mongodb://localhost:27017,localhost:27018,localhost:27019',replicaSet="replicasetkey123", read_preference=ReadPreference.PRIMARY)

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