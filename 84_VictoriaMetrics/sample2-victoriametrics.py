import time
import requests

base = "http://localhost:8428"

# (何分前, センサー名, 計測値)。直近データとして取り込む
samples = [
    (90, "Alice", 10.0),
    (75, "Alice", 12.0),
    (60, "Alice", 11.0),
    (30, "Alice", 20.0),
    (15, "Alice", 22.0),
    (90, "Bob", 5.0),
    (70, "Bob", 7.0),
    (50, "Bob", 9.0),
]


def import_data():
    now = time.time()
    lines = []
    for minutes_ago, sensor, value in samples:
        ts_ns = int((now - minutes_ago * 60) * 1e9)
        lines.append("metrics,sensor={0} value={1} {2}".format(sensor, value, ts_ns))
    requests.post(base + "/write", data="\n".join(lines))
    # 取り込み後、検索可能になるまで少し待つ
    time.sleep(2)


def query_instant(promql):
    res = requests.get(base + "/api/v1/query", params={"query": promql})
    return res.json()["data"]["result"]


def aggregate_search():

    print("=== METRICSQL AGGREGATE TEST ===")

    print("import data")

    import_data()

    print("avg over last 2h per sensor")

    # avg_over_time で過去 2 時間の平均を計算する (時間窓の集計 = ダウンサンプリング)
    result = query_instant("avg_over_time(metrics[2h])")
    for series in result:
        print("Data row =", series["metric"].get("sensor"), "avg =", round(float(series["value"][1]), 2))


if __name__ == "__main__":

    aggregate_search()
