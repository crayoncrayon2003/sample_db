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


def create_index():

    print("=== FULLTEXT TEST ===")

    client = connect()

    print("create index and insert data")

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

    for doc in documents:
        print("Data row =", doc["id"], doc["sender"], doc["message"])


def fuzzy_search():

    print("=== FUZZY SEARCH TEST ===")

    client = connect()

    keyword = "qiuck fpx"

    print("fuzzy search", repr(keyword))

    # fuzziness で綴り間違い (qiuck -> quick, fpx -> fox) も許容して検索する
    body = {"query": {"match": {"message": {"query": keyword, "fuzziness": "AUTO"}}}}
    result = client.search(index=index_name, body=body)
    for hit in result["hits"]["hits"]:
        print("Data row =", hit["_id"], round(hit["_score"], 4), hit["_source"])


if __name__ == "__main__":

    create_index()

    fuzzy_search()
