from pymilvus import MilvusClient

uri = "http://localhost:19530"
collection_name = "sample_collection"
vector_size = 4


def connect():
    return MilvusClient(uri=uri)


def vector_search():

    print("=== VECTOR TEST ===")

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
        {"id": 1, "vector": [0.10, 0.20, 0.30, 0.40], "name": "banana", "quantity": 150},
        {"id": 2, "vector": [0.20, 0.10, 0.40, 0.30], "name": "orange", "quantity": 154},
        {"id": 3, "vector": [0.90, 0.80, 0.70, 0.60], "name": "apple", "quantity": 100},
    ]

    client.insert(collection_name=collection_name, data=data)

    print("search data")

    results = client.search(
        collection_name=collection_name,
        data=[[0.15, 0.15, 0.35, 0.35]],
        limit=3,
        output_fields=["name", "quantity"],
    )

    for hit in results[0]:
        print("Data row =", hit["id"], hit["distance"], hit["entity"])


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    client = connect()

    print("search data with filter (name == apple)")

    results = client.search(
        collection_name=collection_name,
        data=[[0.15, 0.15, 0.35, 0.35]],
        filter='name == "apple"',
        limit=3,
        output_fields=["name", "quantity"],
    )

    for hit in results[0]:
        print("Data row =", hit["id"], hit["distance"], hit["entity"])


if __name__ == "__main__":

    vector_search()

    filtered_search()
