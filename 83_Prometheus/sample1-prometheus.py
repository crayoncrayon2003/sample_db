import time
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

pushgateway = "localhost:9092"
prometheus = "http://localhost:9090"
job = "sample"

# (センサー名, 計測値)。Prometheus は pull 型なので Pushgateway 経由で渡す
readings = [
    ("Alice", 10.0),
    ("Bob", 5.0),
]


def push_metrics():
    registry = CollectorRegistry()
    gauge = Gauge("sample_value", "sample metric value", ["sensor"], registry=registry)
    for sensor, value in readings:
        gauge.labels(sensor=sensor).set(value)
    push_to_gateway(pushgateway, job=job, registry=registry)


def query(promql):
    # Prometheus がスクレイプして値が見えるまで数回リトライする
    for _ in range(15):
        res = requests.get(prometheus + "/api/v1/query", params={"query": promql})
        result = res.json()["data"]["result"]
        if result:
            return result
        time.sleep(1)
    return []


def timeseries_test():

    print("=== TIMESERIES TEST ===")

    print("push data")

    push_metrics()

    print("query data")

    # メトリクス名で検索すると、ラベル (sensor) ごとに最新値が返る
    result = query("sample_value")
    for series in result:
        print("Data row =", series["metric"].get("sensor"), series["value"][1])


if __name__ == "__main__":

    timeseries_test()
