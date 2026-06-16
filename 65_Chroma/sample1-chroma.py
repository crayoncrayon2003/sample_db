import chromadb

host = "localhost"
port = 8000
collection_name = "sample_collection"

fruits = [
    {"id": 1, "name": "banana", "quantity": 150, "vector": [0.10, 0.20, 0.30, 0.40]},
    {"id": 2, "name": "orange", "quantity": 154, "vector": [0.20, 0.10, 0.40, 0.30]},
    {"id": 3, "name": "apple", "quantity": 100, "vector": [0.90, 0.80, 0.70, 0.60]},
]


def connect():
    return chromadb.HttpClient(host=host, port=port)


def vector_search():

    print("=== VECTOR TEST ===")

    client = connect()

    print("create collection")

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    # hnsw:space で距離関数を cosine に指定する
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    print("insert data")

    collection.add(
        ids=[str(f["id"]) for f in fruits],
        embeddings=[f["vector"] for f in fruits],
        metadatas=[{"name": f["name"], "quantity": f["quantity"]} for f in fruits],
    )

    print("search data")

    results = collection.query(
        query_embeddings=[[0.15, 0.15, 0.35, 0.35]],
        n_results=3,
    )
    for id_, dist, meta in zip(results["ids"][0], results["distances"][0], results["metadatas"][0]):
        print("Data row =", id_, round(dist, 4), meta)


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    client = connect()
    collection = client.get_collection(collection_name)

    print("search data with filter (name = apple)")

    results = collection.query(
        query_embeddings=[[0.15, 0.15, 0.35, 0.35]],
        n_results=3,
        where={"name": "apple"},
    )
    for id_, dist, meta in zip(results["ids"][0], results["distances"][0], results["metadatas"][0]):
        print("Data row =", id_, round(dist, 4), meta)


if __name__ == "__main__":

    vector_search()

    filtered_search()
