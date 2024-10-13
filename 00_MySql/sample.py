import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'user',
    'password': 'user',
    'host': 'localhost',
    'port': '3306',
    'database': 'sample_db'
}

def sql():
    print("接続文字列")
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print('Successfully connected to the database')

        cursor = conn.cursor()

        print("テーブル作成")
        cursor.execute("CREATE TABLE IF NOT EXISTS sql_table (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")

        print("テーブルへデータ挿入")
        cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("banana", 150))
        cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("orange", 154))
        cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("apple", 100))
        conn.commit()

        print("テーブルからデータ取得")
        cursor.execute("SELECT * FROM sql_table;")
        rows = cursor.fetchall()
        for row in rows:
            print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

        # Clean up
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f'Error: {err}')
    finally:
        if conn.is_connected():
            conn.close()
            print('Connection closed')


if __name__ == "__main__":
    sql()
    #nosql()
    #exportPARQUET()