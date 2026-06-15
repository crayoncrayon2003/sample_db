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


def index_documents(es):
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


def fulltext_test():

    print("=== FULLTEXT TEST ===")

    es = connect()

    print("create index and insert data")

    index_documents(es)

    print("search 'quick fox'")

    # match クエリは本文を単語に分割し、関連度 (_score) の高い順に返す
    result = es.search(index=index_name, query={"match": {"message": "quick fox"}})
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])

    es.close()


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    es = connect()

    print("search 'fox' with filter (sender = Carol)")

    # 全文検索 (match) と完全一致フィルタ (term) を bool で組み合わせる
    result = es.search(
        index=index_name,
        query={
            "bool": {
                "must": [{"match": {"message": "fox"}}],
                "filter": [{"term": {"sender.keyword": "Carol"}}],
            }
        },
    )
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])

    es.close()


if __name__ == "__main__":

    fulltext_test()

    filtered_search()
