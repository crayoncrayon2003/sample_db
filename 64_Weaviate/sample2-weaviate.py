import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery

collection_name = "Person"

# 各人物を 4 次元の特徴ベクトルで表す
people = [
    {"name": "Alice", "vector": [0.1, 0.9, 0.3, 0.0]},
    {"name": "Bob", "vector": [0.2, 0.8, 0.2, 0.1]},
    {"name": "Carol", "vector": [0.9, 0.1, 0.8, 0.2]},
    {"name": "Dave", "vector": [0.8, 0.2, 0.9, 0.1]},
    {"name": "Eve", "vector": [0.3, 0.7, 0.0, 0.9]},
]


def connect():
    # localhost:8080 (REST) と localhost:50051 (gRPC) に接続する
    return weaviate.connect_to_local()


def create_collection():

    print("=== PERSON VECTOR TEST ===")

    client = connect()

    print("create collection")

    if client.collections.exists(collection_name):
        client.collections.delete(collection_name)

    client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="name", data_type=DataType.TEXT),
        ],
    )
    collection = client.collections.get(collection_name)

    print("insert data")

    for p in people:
        collection.data.insert(properties={"name": p["name"]}, vector=p["vector"])

    for p in people:
        print("Data row =", p["name"])

    client.close()


def similar_search():

    print("=== SIMILAR PERSON SEARCH TEST ===")

    client = connect()
    collection = client.collections.get(collection_name)

    target = "Alice"
    target_vector = next(p["vector"] for p in people if p["name"] == target)

    print("search people similar to", target)

    # 基準人物のベクトルに近い順で返る (自分自身も含まれるので後で除外する)
    results = collection.query.near_vector(
        near_vector=target_vector,
        limit=4,
        return_metadata=MetadataQuery(distance=True),
    )
    for obj in results.objects:
        if obj.properties["name"] == target:
            continue
        print("Data row =", round(obj.metadata.distance, 4), obj.properties)

    client.close()


if __name__ == "__main__":

    create_collection()

    similar_search()
