from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

host = "localhost"
port = 6333
collection_name = "sample_collection"
vector_size = 4


def connect():
    return QdrantClient(host=host, port=port)


def vector_search():

    print("=== VECTOR TEST ===")

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
        PointStruct(
            id=1,
            vector=[0.10, 0.20, 0.30, 0.40],
            payload={"name": "banana", "quantity": 150},
        ),
        PointStruct(
            id=2,
            vector=[0.20, 0.10, 0.40, 0.30],
            payload={"name": "orange", "quantity": 154},
        ),
        PointStruct(
            id=3,
            vector=[0.90, 0.80, 0.70, 0.60],
            payload={"name": "apple", "quantity": 100},
        ),
    ]

    client.upsert(collection_name=collection_name, points=points)

    print("search data")

    results = client.query_points(
        collection_name=collection_name,
        query=[0.15, 0.15, 0.35, 0.35],
        limit=3,
    ).points

    for hit in results:
        print("Data row =", hit.id, hit.score, hit.payload)


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    client = connect()

    print("search data with filter (name = apple)")

    results = client.query_points(
        collection_name=collection_name,
        query=[0.15, 0.15, 0.35, 0.35],
        query_filter=Filter(
            must=[
                FieldCondition(key="name", match=MatchValue(value="apple")),
            ]
        ),
        limit=3,
    ).points

    for hit in results:
        print("Data row =", hit.id, hit.score, hit.payload)


if __name__ == "__main__":

    vector_search()

    filtered_search()
