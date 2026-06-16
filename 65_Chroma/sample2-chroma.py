import chromadb

host = "localhost"
port = 8000
collection_name = "person_collection"

# 各人物を 4 次元の特徴ベクトルで表す
people = [
    {"id": 1, "name": "Alice", "vector": [0.1, 0.9, 0.3, 0.0]},
    {"id": 2, "name": "Bob", "vector": [0.2, 0.8, 0.2, 0.1]},
    {"id": 3, "name": "Carol", "vector": [0.9, 0.1, 0.8, 0.2]},
    {"id": 4, "name": "Dave", "vector": [0.8, 0.2, 0.9, 0.1]},
    {"id": 5, "name": "Eve", "vector": [0.3, 0.7, 0.0, 0.9]},
]


def connect():
    return chromadb.HttpClient(host=host, port=port)


def create_collection():

    print("=== PERSON VECTOR TEST ===")

    client = connect()

    print("create collection")

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    print("insert data")

    collection.add(
        ids=[str(p["id"]) for p in people],
        embeddings=[p["vector"] for p in people],
        metadatas=[{"name": p["name"]} for p in people],
    )

    for p in people:
        print("Data row =", p["id"], p["name"])


def similar_search():

    print("=== SIMILAR PERSON SEARCH TEST ===")

    client = connect()
    collection = client.get_collection(collection_name)

    target = "Alice"
    target_vector = next(p["vector"] for p in people if p["name"] == target)

    print("search people similar to", target)

    # 基準人物のベクトルに近い順で返る (自分自身も含まれるので後で除外する)
    results = collection.query(query_embeddings=[target_vector], n_results=4)
    for id_, dist, meta in zip(results["ids"][0], results["distances"][0], results["metadatas"][0]):
        if meta["name"] == target:
            continue
        print("Data row =", id_, round(dist, 4), meta)


if __name__ == "__main__":

    create_collection()

    similar_search()
