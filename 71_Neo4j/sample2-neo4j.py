from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

# (人物)-[参加]->(作品) の関係。共演 (共同参加) 関係はこの形から導出する
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
    return GraphDatabase.driver(uri, auth=(user, password))


def create_graph():

    print("=== WORK GRAPH TEST ===")

    driver = connect()

    with driver.session() as session:

        print("create nodes and relationships")

        # 既存データをクリアしてから作り直す
        session.run("MATCH (n:Person) DETACH DELETE n;")
        session.run("MATCH (n:Work) DETACH DELETE n;")

        # 人物が作品に参加している (ACTED_IN) という関係を張る
        for person, work in casts:
            session.run(
                """
                MERGE (p:Person {name: $person})
                MERGE (w:Work {title: $work})
                MERGE (p)-[:ACTED_IN]->(w);
                """,
                person=person, work=work,
            )

        print("query persons")

        result = session.run("MATCH (p:Person) RETURN p.name AS name ORDER BY p.name;")
        for record in result:
            print("Data row =", record["name"])

    driver.close()


def co_actor_search():

    print("=== CO-ACTOR SEARCH TEST ===")

    driver = connect()

    with driver.session() as session:

        target = "Alice"

        print("search co-actors of", target)

        # 人物 -> 参加作品 -> その作品に参加する別の人物 をたどる
        result = session.run(
            """
            MATCH (target:Person {name: $target})-[:ACTED_IN]->(w:Work)<-[:ACTED_IN]-(co:Person)
            WHERE co <> target
            RETURN co.name AS name, collect(DISTINCT w.title) AS works
            ORDER BY name;
            """,
            target=target,
        )
        for record in result:
            print("Data row =", record["name"], "via", record["works"])

    driver.close()


if __name__ == "__main__":

    create_graph()

    co_actor_search()
