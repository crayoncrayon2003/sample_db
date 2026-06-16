import duckdb
import numpy as np
import pandas as pd


def make_data(seed=11):
    # 10 日 x 2 地域の売上データ
    rng = np.random.default_rng(seed)
    days = pd.date_range("2026-01-01", periods=10, freq="D")
    rows = []
    for d in days:
        for region in ["east", "west"]:
            rows.append({
                "dt": d.date().isoformat(),
                "region": region,
                "amount": float(rng.integers(50, 150)),
            })
    return pd.DataFrame(rows)


def main():
    df = make_data()
    con = duckdb.connect()
    con.register("data", df)

    print("=== ranking window functions (順位付け) ===")
    rank_q = """
        SELECT dt, region, amount,
            rank()         OVER (PARTITION BY region ORDER BY amount DESC) AS rnk,
            ntile(4)       OVER (PARTITION BY region ORDER BY amount)      AS quartile,
            round(percent_rank() OVER (PARTITION BY region ORDER BY amount), 3) AS pct_rank
        FROM data
        ORDER BY region, amount DESC
    """
    print(con.sql(rank_q).df())

    print("\n=== moving average (3 期移動平均) ===")
    mov_q = """
        SELECT dt, region, amount,
            round(avg(amount) OVER (
                PARTITION BY region ORDER BY dt
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ), 2) AS moving_avg_3
        FROM data
        ORDER BY region, dt
    """
    print(con.sql(mov_q).df())

    print("\n=== ROLLUP (地域別＋総計の小計) ===")
    rollup_q = """
        SELECT region, sum(amount) AS total
        FROM data
        GROUP BY ROLLUP(region)
        ORDER BY region
    """
    print(con.sql(rollup_q).df())


if __name__ == "__main__":
    main()
