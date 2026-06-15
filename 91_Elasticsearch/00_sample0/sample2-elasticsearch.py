from elasticsearch import Elasticsearch

host = "http://localhost:9200"
index_name = "messages"

# (id, 送信者, 本文) のドキュメント
documents = [
    {"id": 1, "sender": "Alice", "message": "the quick brown fox"},
    {"id": 2, "sender": "Bob", "message": "the lazy dog sleeps all day"},
    {"id": 3, "sender": "Carol", "message": "a quick red fox runs away"},
    {"id": 4, "sender": "Dave", "message": "brown bears love sweet honey"},
]


def connect():
    return Elasticsearch(host)


def create_index():

    print("=== FULLTEXT TEST ===")

    es = connect()

    print("create index and insert data")

    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name)

    for doc in documents:
        es.index(
            index=index_name,
            id=doc["id"],
            document={"sender": doc["sender"], "message": doc["message"]},
        )
    # 検索可能になるまで反映を待つ
    es.indices.refresh(index=index_name)

    for doc in documents:
        print("Data row =", doc["id"], doc["sender"], doc["message"])

    es.close()


def fuzzy_search():

    print("=== FUZZY SEARCH TEST ===")

    es = connect()

    keyword = "qiuck fpx"

    print("fuzzy search", repr(keyword))

    # fuzziness で綴り間違い (qiuck -> quick, fpx -> fox) も許容して検索する
    result = es.search(
        index=index_name,
        query={"match": {"message": {"query": keyword, "fuzziness": "AUTO"}}},
    )
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])

    es.close()


if __name__ == "__main__":

    create_index()

    fuzzy_search()
