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


def aggregate_search():

    print("=== PROMQL AGGREGATE TEST ===")

    print("push data")

    push_metrics()

    print("avg over time (1m) per sensor")

    # avg_over_time で過去 1 分間の平均を計算する (PromQL による時間窓集計)
    result = query("avg_over_time(sample_value[1m])")
    for series in result:
        print("Data row =", series["metric"].get("sensor"), "avg =", round(float(series["value"][1]), 2))

    print("sum over all sensors")

    # ラベルをまたいで合計する集約
    result = query("sum(sample_value)")
    for series in result:
        print("Data row = total", series["value"][1])


if __name__ == "__main__":

    aggregate_search()
