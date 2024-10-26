import psycopg2
from psycopg2.extras import Json

host = "localhost"
dbname = "test"
user = "user"
password = "user"

def sql():
    print("connection string")
    conn_string = "host={0} user={1} password={2}".format(host, user, password)
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    print("create table")
    cursor.execute("CREATE TABLE IF NOT EXISTS sql_table (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")

    print("set data")
    cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("banana", 150))
    cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("orange", 154))
    cursor.execute("INSERT INTO sql_table (name, quantity) VALUES (%s, %s);", ("apple", 100))
    conn.commit()

    print("get data")
    cursor.execute("SELECT * FROM sql_table;")
    rows = cursor.fetchall()
    for row in rows:
        print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

    # Clean up
    cursor.close()
    conn.close()

def nosql():
    print("connection string")
    conn_string = "host={0} user={1} password={2}".format(host, user, password)
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    print("create table")
    cursor.execute("CREATE TABLE IF NOT EXISTS nosql_table (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER, info JSONB);")

    print("set data")
    cursor.execute("INSERT INTO nosql_table (name, quantity, info) VALUES (%s, %s, %s);", ("banana", 150, Json({"key1":10, "key2": "update"})))
    cursor.execute("INSERT INTO nosql_table (name, quantity, info) VALUES (%s, %s, %s);", ("orange", 154, Json({"key1":20, "key2": "update"})))
    cursor.execute("INSERT INTO nosql_table (name, quantity, info) VALUES (%s, %s, %s);", ("apple" , 100, Json({"key1":30, "key2": "update"})))
    conn.commit()

    print("get data")
    cursor.execute("SELECT * FROM nosql_table;")
    rows = cursor.fetchall()
    for row in rows:
        print("Data row = (%s, %s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]), str(row[3])))

    # Clean up
    cursor.close()
    conn.close()

def exportPARQUET():
    print("connection string")
    conn_string = "host={0} user={1} password={2}".format(host, user, password)
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    print("outup PARQUET")
    cursor.execute("EXPORT TO PARQUET (directory = \'./PARQUET\') AS SELECT * FROM nosql_table;")

    # Clean up
    cursor.close()
    conn.close()

if __name__ == "__main__":
    sql()
    #nosql()
    #exportPARQUET()