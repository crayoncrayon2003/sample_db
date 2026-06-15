from elasticsearch import Elasticsearch

# === Batch パターン (Elasticsearch から読み取り) ===
# 検索用側 (Elasticsearch) を確認する。
# Batch では batch_sync.py を実行するまで反映されない。
# app.py で書いただけでは ES は空のまま (定期実行の間隔ぶん遅れる)。

ES_HOST = "http://localhost:9200"
INDEX = "products"


def main():
    es = Elasticsearch(ES_HOST)

    print("=== READ FROM Elasticsearch ===")

    if not es.indices.exists(index=INDEX):
        print("(index not created yet)")
        es.close()
        return

    es.indices.refresh(index=INDEX)

    print("all documents (match_all)")
    result = es.search(index=INDEX, query={"match_all": {}})
    hits = result["hits"]["hits"]
    if not hits:
        print("(empty -- batch_sync.py をまだ実行していない可能性があります)")
    for hit in hits:
        print("Data row =", hit["_id"], hit["_source"])

    print("full-text search: 'laptop'")
    result = es.search(index=INDEX, query={"match": {"description": "laptop"}})
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])

    es.close()


if __name__ == "__main__":
    main()
