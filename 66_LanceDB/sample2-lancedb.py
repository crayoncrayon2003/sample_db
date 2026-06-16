import lancedb

db_path = "./lancedb_data"
table_name = "people"

# 各人物を 4 次元の特徴ベクトルで表す
people = [
    {"vector": [0.1, 0.9, 0.3, 0.0], "name": "Alice"},
    {"vector": [0.2, 0.8, 0.2, 0.1], "name": "Bob"},
    {"vector": [0.9, 0.1, 0.8, 0.2], "name": "Carol"},
    {"vector": [0.8, 0.2, 0.9, 0.1], "name": "Dave"},
    {"vector": [0.3, 0.7, 0.0, 0.9], "name": "Eve"},
]


def connect():
    # サーバ不要。ローカルのディレクトリにデータを保存する組み込み型
    return lancedb.connect(db_path)


def create_table():

    print("=== PERSON VECTOR TEST ===")

    db = connect()

    print("create table")

    table = db.create_table(table_name, data=people, mode="overwrite")

    for p in people:
        print("Data row =", p["name"])

    return table


def similar_search():

    print("=== SIMILAR PERSON SEARCH TEST ===")

    db = connect()
    table = db.open_table(table_name)

    target = "Alice"
    target_vector = next(p["vector"] for p in people if p["name"] == target)

    print("search people similar to", target)

    # 基準人物のベクトルに近い順で取得する (自分自身も含まれるので後で除外する)
    results = table.search(target_vector).metric("cosine").limit(4).to_list()
    for row in results:
        if row["name"] == target:
            continue
        print("Data row =", round(row["_distance"], 4), {"name": row["name"]})


if __name__ == "__main__":

    create_table()

    similar_search()
