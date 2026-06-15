from elasticsearch import Elasticsearch

# === CDC パターン (Elasticsearch から読み取り) ===
# 検索用側 (Elasticsearch) を確認する。
# CDC では Debezium が WAL を拾い、Redis Streams 経由で subscriber.py が
# 反映するまで時間差がある。subscriber.py を止めていると 0 件のことがある。

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
        print("(empty -- subscriber.py がまだ反映していない可能性があります)")
    for hit in hits:
        print("Data row =", hit["_id"], hit["_source"])

    print("full-text search: 'laptop'")
    result = es.search(index=INDEX, query={"match": {"description": "laptop"}})
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])

    es.close()


if __name__ == "__main__":
    main()
