from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"


def connect():
    return GraphDatabase.driver(uri, auth=(user, password))


def create_graph():

    print("=== GRAPH TEST ===")

    driver = connect()

    with driver.session() as session:

        print("create nodes")

        # 既存データをクリアしてから作り直す
        session.run("MATCH (n:Fruit) DETACH DELETE n;")

        session.run(
            """
            CREATE (:Fruit {name: $n1, quantity: $q1}),
                   (:Fruit {name: $n2, quantity: $q2}),
                   (:Fruit {name: $n3, quantity: $q3});
            """,
            n1="banana", q1=150,
            n2="orange", q2=154,
            n3="apple", q3=100,
        )

        print("create relationships")

        # banana -> orange -> apple という NEXT リレーションを張る
        session.run(
            """
            MATCH (b:Fruit {name: 'banana'}), (o:Fruit {name: 'orange'})
            CREATE (b)-[:NEXT]->(o);
            """
        )
        session.run(
            """
            MATCH (o:Fruit {name: 'orange'}), (a:Fruit {name: 'apple'})
            CREATE (o)-[:NEXT]->(a);
            """
        )

        print("query nodes")

        result = session.run(
            "MATCH (f:Fruit) RETURN f.name AS name, f.quantity AS quantity ORDER BY f.quantity;"
        )
        for record in result:
            print("Data row =", record["name"], record["quantity"])

    driver.close()


def traverse_graph():

    print("=== TRAVERSE TEST ===")

    driver = connect()

    with driver.session() as session:

        print("query path from banana")

        # banana から NEXT をたどって到達できるノードを取得
        result = session.run(
            """
            MATCH path = (start:Fruit {name: 'banana'})-[:NEXT*]->(end:Fruit)
            RETURN end.name AS name, end.quantity AS quantity, length(path) AS hops
            ORDER BY hops;
            """
        )
        for record in result:
            print("Data row =", record["name"], record["quantity"], "hops =", record["hops"])

    driver.close()


if __name__ == "__main__":

    create_graph()

    traverse_graph()
