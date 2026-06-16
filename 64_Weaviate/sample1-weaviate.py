import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery, Filter

collection_name = "Fruit"

fruits = [
    {"name": "banana", "quantity": 150, "vector": [0.10, 0.20, 0.30, 0.40]},
    {"name": "orange", "quantity": 154, "vector": [0.20, 0.10, 0.40, 0.30]},
    {"name": "apple", "quantity": 100, "vector": [0.90, 0.80, 0.70, 0.60]},
]


def connect():
    # localhost:8080 (REST) と localhost:50051 (gRPC) に接続する
    return weaviate.connect_to_local()


def vector_search():

    print("=== VECTOR TEST ===")

    client = connect()

    print("create collection")

    if client.collections.exists(collection_name):
        client.collections.delete(collection_name)

    # ベクトルは自分で渡すので vectorizer は none にする
    client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="name", data_type=DataType.TEXT),
            Property(name="quantity", data_type=DataType.INT),
        ],
    )
    collection = client.collections.get(collection_name)

    print("insert data")

    for f in fruits:
        collection.data.insert(
            properties={"name": f["name"], "quantity": f["quantity"]},
            vector=f["vector"],
        )

    print("search data")

    results = collection.query.near_vector(
        near_vector=[0.15, 0.15, 0.35, 0.35],
        limit=3,
        return_metadata=MetadataQuery(distance=True),
    )
    for obj in results.objects:
        print("Data row =", round(obj.metadata.distance, 4), obj.properties)

    client.close()


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    client = connect()
    collection = client.collections.get(collection_name)

    print("search data with filter (name = apple)")

    results = collection.query.near_vector(
        near_vector=[0.15, 0.15, 0.35, 0.35],
        filters=Filter.by_property("name").equal("apple"),
        limit=3,
        return_metadata=MetadataQuery(distance=True),
    )
    for obj in results.objects:
        print("Data row =", round(obj.metadata.distance, 4), obj.properties)

    client.close()


if __name__ == "__main__":

    vector_search()

    filtered_search()
