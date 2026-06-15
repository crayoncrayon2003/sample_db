from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

url = "ws://localhost:8182/gremlin"


def connect():
    connection = DriverRemoteConnection(url, "g")
    g = traversal().with_remote(connection)
    return g, connection


def create_graph():

    print("=== GRAPH TEST ===")

    g, connection = connect()

    print("create nodes")

    # 既存データをクリアしてから作り直す
    g.V().drop().iterate()

    # JanusGraph の頂点 ID は独自型のため、頂点を返す .next() ではなく
    # .iterate() で実行する (返り値をデシリアライズしない)
    g.addV("fruit").property("name", "banana").property("quantity", 150).iterate()
    g.addV("fruit").property("name", "orange").property("quantity", 154).iterate()
    g.addV("fruit").property("name", "apple").property("quantity", 100).iterate()

    print("create relationships")

    # banana -> orange -> apple という next エッジを張る
    g.V().has("fruit", "name", "banana").as_("a") \
        .V().has("fruit", "name", "orange").as_("b") \
        .addE("next").from_("a").to("b").iterate()
    g.V().has("fruit", "name", "orange").as_("a") \
        .V().has("fruit", "name", "apple").as_("b") \
        .addE("next").from_("a").to("b").iterate()

    print("query nodes")

    results = g.V().hasLabel("fruit").order().by("quantity") \
        .valueMap("name", "quantity").toList()
    for row in results:
        print("Data row =", row["name"][0], row["quantity"][0])

    connection.close()


def traverse_graph():

    print("=== TRAVERSE TEST ===")

    g, connection = connect()

    print("query path from banana")

    # banana から next をたどって到達できるノードを取得
    results = g.V().has("fruit", "name", "banana") \
        .repeat(__.out("next")).emit() \
        .valueMap("name", "quantity").toList()
    for row in results:
        print("Data row =", row["name"][0], row["quantity"][0])

    connection.close()


if __name__ == "__main__":

    create_graph()

    traverse_graph()
