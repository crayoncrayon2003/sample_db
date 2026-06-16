import sqlite3

DB_PATH = "sample.db"


def sql():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("create table")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sql_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
    )

    print("reset data")
    cursor.execute("DELETE FROM sql_table;")

    print("set data")
    cursor.executemany(
        "INSERT INTO sql_table (name, quantity) VALUES (?, ?);",
        [
            ("banana", 150),
            ("orange", 154),
            ("apple", 100),
        ],
    )
    conn.commit()

    print("get data")
    cursor.execute("SELECT * FROM sql_table ORDER BY id;")
    rows = cursor.fetchall()
    for row in rows:
        print("Data row = (%s, %s, %s)" % (str(row[0]), str(row[1]), str(row[2])))

    cursor.close()
    conn.close()


if __name__ == "__main__":
    sql()
