import sys
import psycopg2

# === Batch パターン (アプリ) ===
# アプリは PostgreSQL に書くだけ。ES は知らない。
# 反映は batch_sync.py が定期的に SELECT して行う。
#
# 使い方:
#   python app.py init    … テーブル作成 + 初期データ投入
#   python app.py update  … 1 行更新 (差分同期の確認用)

PG = dict(host="localhost", port=5432, dbname="test", user="user", password="user")

# (id, name, description, quantity)
products = [
    (1, "Apple MacBook", "lightweight aluminum laptop with long battery life", 10),
    (2, "Banana Phone", "yellow curved smartphone with a retro design", 25),
    (3, "Orange Tablet", "vivid display tablet for reading and drawing", 15),
]


def init(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products;")
    cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            description TEXT,
            quantity INTEGER,
            updated_at TIMESTAMP NOT NULL DEFAULT now()
        );
    """)
    # 更新時に updated_at を自動更新する (差分同期のキーになる)
    cur.execute("""
        CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    cur.execute("""
        CREATE TRIGGER trg_updated_at BEFORE UPDATE ON products
        FOR EACH ROW EXECUTE FUNCTION set_updated_at();
    """)
    conn.commit()

    for row in products:
        cur.execute(
            "INSERT INTO products (id, name, description, quantity) VALUES (%s, %s, %s, %s);",
            row,
        )
        print("insert =", row[0], row[1])
    conn.commit()
    cur.close()


def update(conn):
    cur = conn.cursor()
    cur.execute("UPDATE products SET quantity = 999 WHERE id = 1;")
    conn.commit()
    print("update = 1 (quantity -> 999)")
    cur.close()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "init"
    conn = psycopg2.connect(**PG)

    if mode == "init":
        init(conn)
    elif mode == "update":
        update(conn)
    else:
        print("usage: python app.py [init|update]")

    conn.close()


if __name__ == "__main__":
    main()
