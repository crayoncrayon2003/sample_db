from opensearchpy import OpenSearch

host = "localhost"
port = 9201
index_name = "messages"

# (id, 送信者, 本文) のドキュメント
documents = [
    {"id": 1, "sender": "Alice", "message": "the quick brown fox"},
    {"id": 2, "sender": "Bob", "message": "the lazy dog sleeps all day"},
    {"id": 3, "sender": "Carol", "message": "a quick red fox runs away"},
    {"id": 4, "sender": "Dave", "message": "brown bears love sweet honey"},
]


def connect():
    # セキュリティプラグインを無効化しているので SSL / 認証なしで接続する
    return OpenSearch(hosts=[{"host": host, "port": port}], use_ssl=False)


def index_documents(client):
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
    client.indices.create(index=index_name)

    for doc in documents:
        client.index(
            index=index_name,
            id=doc["id"],
            body={"sender": doc["sender"], "message": doc["message"]},
        )
    # 検索可能になるまで反映を待つ
    client.indices.refresh(index=index_name)


def fulltext_test():

    print("=== FULLTEXT TEST ===")

    client = connect()

    print("create index and insert data")

    index_documents(client)

    print("search 'quick fox'")

    # match クエリは本文を単語に分割し、関連度 (_score) の高い順に返す
    body = {"query": {"match": {"message": "quick fox"}}}
    result = client.search(index=index_name, body=body)
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    client = connect()

    print("search 'fox' with filter (sender = Carol)")

    # 全文検索 (match) と完全一致フィルタ (term) を bool で組み合わせる
    body = {
        "query": {
            "bool": {
                "must": [{"match": {"message": "fox"}}],
                "filter": [{"term": {"sender.keyword": "Carol"}}],
            }
        }
    }
    result = client.search(index=index_name, body=body)
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])


if __name__ == "__main__":

    fulltext_test()

    filtered_search()
