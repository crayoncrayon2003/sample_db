from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import P
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

url = "ws://localhost:8182/gremlin"

# (人物名, 作品名) の参加関係
casts = [
    ("Alice", "Alpha"),
    ("Bob", "Alpha"),
    ("Carol", "Alpha"),
    ("Alice", "Beta"),
    ("Carol", "Beta"),
    ("Alice", "Gamma"),
    ("Dave", "Gamma"),
]


def connect():
    connection = DriverRemoteConnection(url, "g")
    g = traversal().with_remote(connection)
    return g, connection


def create_graph():

    print("=== WORK GRAPH TEST ===")

    g, connection = connect()

    print("create nodes")

    # 既存データをクリアしてから作り直す
    g.V().drop().iterate()

    persons = sorted({person for person, _ in casts})
    works = sorted({work for _, work in casts})
    for name in persons:
        g.addV("person").property("name", name).iterate()
    for title in works:
        g.addV("work").property("title", title).iterate()

    print("create relationships")

    # 人物 -> 作品 の acted_in エッジを張る
    for person, work in casts:
        g.V().has("person", "name", person).as_("a") \
            .V().has("work", "title", work).as_("w") \
            .addE("acted_in").from_("a").to("w").iterate()

    print("query persons")

    results = g.V().hasLabel("person").order().by("name").values("name").toList()
    for name in results:
        print("Data row =", name)

    connection.close()


def co_actor_search():

    print("=== CO-ACTOR SEARCH TEST ===")

    g, connection = connect()

    target = "Alice"

    print("search co-actors of", target)

    # 人物 -> 参加作品 (out) -> 共同参加者 (in) をたどり、本人を除外する
    results = g.V().has("person", "name", target) \
        .out("acted_in").in_("acted_in") \
        .where(__.values("name").is_(P.neq(target))) \
        .dedup().values("name").order().toList()
    for name in results:
        print("Data row =", name)

    connection.close()


if __name__ == "__main__":

    create_graph()

    co_actor_search()
