import psycopg2

# === Dual Write パターン (PostgreSQL から読み取り) ===
# 正データ側 (PostgreSQL) に何が入っているかを確認する。
# こちらは SQL で行を取得する (全文検索のスコアなどはない)。

PG = dict(host="localhost", port=5432, dbname="test", user="user", password="user")


def main():
    conn = psycopg2.connect(**PG)
    cur = conn.cursor()

    print("=== READ FROM PostgreSQL ===")

    cur.execute("SELECT id, name, description, quantity FROM products ORDER BY id;")
    for row in cur.fetchall():
        print("Data row =", row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
