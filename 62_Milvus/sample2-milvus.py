from pymilvus import MilvusClient

uri = "http://localhost:19530"
collection_name = "person_collection"
vector_size = 4

# 各人物を 4 次元の特徴ベクトルで表す
people = [
    {"id": 1, "name": "Alice", "vector": [0.1, 0.9, 0.3, 0.0]},
    {"id": 2, "name": "Bob", "vector": [0.2, 0.8, 0.2, 0.1]},
    {"id": 3, "name": "Carol", "vector": [0.9, 0.1, 0.8, 0.2]},
    {"id": 4, "name": "Dave", "vector": [0.8, 0.2, 0.9, 0.1]},
    {"id": 5, "name": "Eve", "vector": [0.3, 0.7, 0.0, 0.9]},
]


def connect():
    return MilvusClient(uri=uri)


def create_collection():

    print("=== PERSON VECTOR TEST ===")

    client = connect()

    print("create collection")

    if client.has_collection(collection_name):
        client.drop_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        dimension=vector_size,
        metric_type="COSINE",
    )

    print("insert data")

    data = [
        {"id": p["id"], "vector": p["vector"], "name": p["name"]}
        for p in people
    ]

    client.insert(collection_name=collection_name, data=data)

    for p in people:
        print("Data row =", p["id"], p["name"])


def similar_search():

    print("=== SIMILAR PERSON SEARCH TEST ===")

    client = connect()

    target = "Alice"
    target_id = next(p["id"] for p in people if p["name"] == target)
    target_vector = next(p["vector"] for p in people if p["name"] == target)

    print("search people similar to", target)

    # 基準人物のベクトルに近い別の人物を探す (filter で自分自身を除外)
    results = client.search(
        collection_name=collection_name,
        data=[target_vector],
        filter="id != {0}".format(target_id),
        limit=3,
        output_fields=["name"],
    )

    for hit in results[0]:
        print("Data row =", hit["id"], hit["distance"], hit["entity"])


if __name__ == "__main__":

    create_collection()

    similar_search()
