import mysql.connector

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': '4000'
}

def sql():
    conn = None

    try:
        conn = mysql.connector.connect(**config)

        if conn.is_connected():
            print("Connected to TiDB")

        cursor = conn.cursor()

        print("create database")
        cursor.execute("CREATE DATABASE IF NOT EXISTS sample_db")

        print("use database")
        cursor.execute("USE sample_db")

        print("create table")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sql_table (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            quantity INT
        )
        """)

        print("insert data")

        data = [
            ("banana",150),
            ("orange",154),
            ("apple",100)
        ]

        cursor.executemany(
            "INSERT INTO sql_table (name, quantity) VALUES (%s,%s)",
            data
        )

        conn.commit()

        print("select data")

        cursor.execute("SELECT * FROM sql_table")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn and conn.is_connected():
            conn.close()
            print("Connection closed")

if __name__ == "__main__":
    sql()