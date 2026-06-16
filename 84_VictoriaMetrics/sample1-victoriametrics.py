import time
from datetime import datetime, timezone
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
        # InfluxDB line protocol: measurement,tag=v field=v timestamp(ns)
        lines.append("metrics,sensor={0} value={1} {2}".format(sensor, value, ts_ns))
    requests.post(base + "/write", data="\n".join(lines))
    # 取り込み後、検索可能になるまで少し待つ
    time.sleep(2)


def query_range(promql, minutes, step):
    end = time.time()
    start = end - minutes * 60
    res = requests.get(base + "/api/v1/query_range", params={
        "query": promql, "start": start, "end": end, "step": step,
    })
    return res.json()["data"]["result"]


def timeseries_test():

    print("=== TIMESERIES TEST ===")

    print("import data")

    import_data()

    print("query data")

    # 過去 2 時間の範囲を 15 分刻みで取得する
    result = query_range("metrics", 120, "15m")
    for series in result:
        sensor = series["metric"].get("sensor")
        for ts, value in series["values"]:
            dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
            print("Data row =", dt, sensor, value)


if __name__ == "__main__":

    timeseries_test()
