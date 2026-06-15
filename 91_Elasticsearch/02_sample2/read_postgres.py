import psycopg2

# === Queue パターン (PostgreSQL から読み取り) ===
# 正データ側 (PostgreSQL) を確認する。
# app.py を実行した直後は、PostgreSQL には即座にデータが入っている。

PG = dict(host="localhost", port=5432, dbname="test", user="user", password="user")


def main():
    conn = psycopg2.connect(**PG)
    cur = conn.cursor()

    print("=== READ FROM PostgreSQL ===")

    cur.execute("SELECT id, name, description, quantity FROM products ORDER BY id;")
    rows = cur.fetchall()
    if not rows:
        print("(empty)")
    for row in rows:
        print("Data row =", row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
