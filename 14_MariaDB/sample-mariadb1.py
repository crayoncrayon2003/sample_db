import mysql.connector

config = {
    "user": "user",
    "password": "user",
    "host": "127.0.0.1",
    "port": "3307",
    "database": "sample_db",
}


def sql():
    conn = mysql.connector.connect(**config)
    try:
        if conn.is_connected():
            print("Successfully connected to the database")

        cursor = conn.cursor()

        print("create table")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sql_table (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                quantity INTEGER
            );
            """
        )

        print("reset data")
        cursor.execute("DELETE FROM sql_table;")

        print("set data")
        cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("banana", 150))
        cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("orange", 154))
        cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("apple", 100))
        conn.commit()

        print("get data")
        cursor.execute("SELECT * FROM sql_table ORDER BY id;")
        rows = cursor.fetchall()
        for row in rows:
            print("Data row = (%s, %s, %s)" % (str(row[0]), str(row[1]), str(row[2])))

        cursor.close()
    finally:
        if conn.is_connected():
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    sql()
