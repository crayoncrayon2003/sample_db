from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

host = "localhost"
port = 6333
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
    return QdrantClient(host=host, port=port)


def create_collection():

    print("=== PERSON VECTOR TEST ===")

    client = connect()

    print("create collection")

    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

    print("insert data")

    points = [
        PointStruct(id=p["id"], vector=p["vector"], payload={"name": p["name"]})
        for p in people
    ]

    client.upsert(collection_name=collection_name, points=points)

    for p in people:
        print("Data row =", p["id"], p["name"])


def similar_search():

    print("=== SIMILAR PERSON SEARCH TEST ===")

    client = connect()

    target = "Alice"
    target_id = next(p["id"] for p in people if p["name"] == target)

    print("search people similar to", target)

    # query に既存の点 ID を渡すと、その人物のベクトルに近い順で返る
    # (自分自身も含まれるので後で除外する)
    results = client.query_points(
        collection_name=collection_name,
        query=target_id,
        limit=4,
    ).points

    for hit in results:
        if hit.id == target_id:
            continue
        print("Data row =", hit.id, round(hit.score, 4), hit.payload)


if __name__ == "__main__":

    create_collection()

    similar_search()
