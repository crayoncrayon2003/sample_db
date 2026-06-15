from arango import ArangoClient

host = "http://localhost:8529"
user = "root"
password = "password"
dbname = "test"
graph_name = "fruit_graph"


def connect():
    client = ArangoClient(hosts=host)

    # test データベースが無ければ作成する
    sys_db = client.db("_system", username=user, password=password)
    if not sys_db.has_database(dbname):
        sys_db.create_database(dbname)

    return client.db(dbname, username=user, password=password)


def create_graph():

    print("=== GRAPH TEST ===")

    db = connect()

    print("create graph")

    # 既存のグラフ / コレクションをクリアしてから作り直す
    if db.has_graph(graph_name):
        db.delete_graph(graph_name, drop_collections=True)

    graph = db.create_graph(graph_name)
    fruit = graph.create_vertex_collection("fruit")
    nxt = graph.create_edge_definition(
        edge_collection="next",
        from_vertex_collections=["fruit"],
        to_vertex_collections=["fruit"],
    )

    print("create nodes")

    fruit.insert({"_key": "banana", "name": "banana", "quantity": 150})
    fruit.insert({"_key": "orange", "name": "orange", "quantity": 154})
    fruit.insert({"_key": "apple", "name": "apple", "quantity": 100})

    print("create relationships")

    # banana -> orange -> apple という next エッジを張る
    nxt.insert({"_from": "fruit/banana", "_to": "fruit/orange"})
    nxt.insert({"_from": "fruit/orange", "_to": "fruit/apple"})

    print("query nodes")

    cursor = db.aql.execute(
        "FOR f IN fruit SORT f.quantity RETURN {name: f.name, quantity: f.quantity}"
    )
    for doc in cursor:
        print("Data row =", doc["name"], doc["quantity"])


def traverse_graph():

    print("=== TRAVERSE TEST ===")

    db = connect()

    print("query path from banana")

    # banana から next をたどって到達できるノードを取得
    cursor = db.aql.execute(
        """
        FOR v, e, p IN 1..10 OUTBOUND 'fruit/banana' next
            RETURN {name: v.name, quantity: v.quantity, hops: LENGTH(p.edges)}
        """
    )
    for doc in cursor:
        print("Data row =", doc["name"], doc["quantity"], "hops =", doc["hops"])


if __name__ == "__main__":

    create_graph()

    traverse_graph()
