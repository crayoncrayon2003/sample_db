import lancedb

db_path = "./lancedb_data"
table_name = "fruits"

fruits = [
    {"vector": [0.10, 0.20, 0.30, 0.40], "name": "banana", "quantity": 150},
    {"vector": [0.20, 0.10, 0.40, 0.30], "name": "orange", "quantity": 154},
    {"vector": [0.90, 0.80, 0.70, 0.60], "name": "apple", "quantity": 100},
]


def connect():
    # サーバ不要。ローカルのディレクトリにデータを保存する組み込み型
    return lancedb.connect(db_path)


def vector_search():

    print("=== VECTOR TEST ===")

    db = connect()

    print("create table")

    # mode="overwrite" で既存テーブルを作り直す
    table = db.create_table(table_name, data=fruits, mode="overwrite")

    print("search data")

    # cosine 距離で近い順に取得する (_distance が小さいほど類似)
    results = table.search([0.15, 0.15, 0.35, 0.35]).metric("cosine").limit(3).to_list()
    for row in results:
        print("Data row =", round(row["_distance"], 4), {"name": row["name"], "quantity": row["quantity"]})


def filtered_search():

    print("=== FILTERED SEARCH TEST ===")

    db = connect()
    table = db.open_table(table_name)

    print("search data with filter (name = apple)")

    # where に SQL 風の条件を渡す。prefilter=True で検索前に絞り込む
    results = (
        table.search([0.15, 0.15, 0.35, 0.35])
        .metric("cosine")
        .where("name = 'apple'", prefilter=True)
        .limit(3)
        .to_list()
    )
    for row in results:
        print("Data row =", round(row["_distance"], 4), {"name": row["name"], "quantity": row["quantity"]})


if __name__ == "__main__":

    vector_search()

    filtered_search()
