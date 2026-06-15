from arango import ArangoClient

host = "http://localhost:8529"
user = "root"
password = "password"
dbname = "test"
graph_name = "work_graph"

# (人物 _key, 人物名) と (作品 _key, 作品名)
persons = [
    ("alice", "Alice"),
    ("bob", "Bob"),
    ("carol", "Carol"),
    ("dave", "Dave"),
]
works = [
    ("alpha", "Alpha"),
    ("beta", "Beta"),
    ("gamma", "Gamma"),
]
# (人物 _key)-[acted_in]->(作品 _key)
casts = [
    ("alice", "alpha"),
    ("bob", "alpha"),
    ("carol", "alpha"),
    ("alice", "beta"),
    ("carol", "beta"),
    ("alice", "gamma"),
    ("dave", "gamma"),
]


def connect():
    client = ArangoClient(hosts=host)

    # test データベースが無ければ作成する
    sys_db = client.db("_system", username=user, password=password)
    if not sys_db.has_database(dbname):
        sys_db.create_database(dbname)

    return client.db(dbname, username=user, password=password)


def create_graph():

    print("=== WORK GRAPH TEST ===")

    db = connect()

    print("create graph")

    # 既存のグラフ / コレクションをクリアしてから作り直す
    if db.has_graph(graph_name):
        db.delete_graph(graph_name, drop_collections=True)

    graph = db.create_graph(graph_name)
    person = graph.create_vertex_collection("person")
    work = graph.create_vertex_collection("work")
    acted_in = graph.create_edge_definition(
        edge_collection="acted_in",
        from_vertex_collections=["person"],
        to_vertex_collections=["work"],
    )

    print("create nodes")

    for key, name in persons:
        person.insert({"_key": key, "name": name})
    for key, title in works:
        work.insert({"_key": key, "title": title})

    print("create relationships")

    # 人物 -> 作品 の参加エッジを張る
    for person_key, work_key in casts:
        acted_in.insert({"_from": "person/" + person_key, "_to": "work/" + work_key})

    print("query persons")

    cursor = db.aql.execute("FOR p IN person SORT p.name RETURN p.name")
    for name in cursor:
        print("Data row =", name)


def co_actor_search():

    print("=== CO-ACTOR SEARCH TEST ===")

    db = connect()

    target_key = "alice"

    print("search co-actors of", target_key)

    # 人物 -> 参加作品 (OUTBOUND) -> 共同参加者 (INBOUND) をたどり、本人を除外する
    cursor = db.aql.execute(
        """
        FOR w IN 1..1 OUTBOUND CONCAT('person/', @target) acted_in
            FOR co IN 1..1 INBOUND w._id acted_in
                FILTER co._key != @target
                COLLECT name = co.name INTO works = w.title
                RETURN {name: name, works: UNIQUE(works)}
        """,
        bind_vars={"target": target_key},
    )
    for doc in cursor:
        print("Data row =", doc["name"], "via", doc["works"])


if __name__ == "__main__":

    create_graph()

    co_actor_search()
