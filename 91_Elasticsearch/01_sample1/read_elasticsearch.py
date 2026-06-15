from elasticsearch import Elasticsearch

# === Dual Write パターン (Elasticsearch から読み取り) ===
# 検索用側 (Elasticsearch) に何が入っているかを確認する。
# こちらは全文検索ができる (match クエリは関連度 _score 順に返す)。

ES_HOST = "http://localhost:9200"
INDEX = "products"


def main():
    es = Elasticsearch(ES_HOST)

    print("=== READ FROM Elasticsearch ===")

    print("all documents (match_all)")
    result = es.search(index=INDEX, query={"match_all": {}})
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], hit["_source"])

    print("full-text search: 'laptop'")
    result = es.search(index=INDEX, query={"match": {"description": "laptop"}})
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])

    es.close()


if __name__ == "__main__":
    main()
