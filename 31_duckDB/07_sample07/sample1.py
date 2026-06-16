import duckdb
import numpy as np
import pandas as pd


def make_data(seed=99):
    # 大きめ（1 万件）のデータで標本抽出・近似集計の効果を見る
    rng = np.random.default_rng(seed)
    n = 10000
    return pd.DataFrame({
        "id": np.arange(n),
        "value": rng.normal(100, 15, n),
    })


def main():
    df = make_data()
    con = duckdb.connect()
    con.register("data", df)

    print("=== full data (全体) ===")
    print(con.sql("SELECT count(*) AS n, round(avg(value), 3) AS mean FROM data").df())

    print("\n=== sampling (標本抽出) ===")
    # 10% のベルヌーイ標本（行単位で抽出。system だとチャンク単位になる）
    print(con.sql("""
        SELECT count(*) AS sample_n, round(avg(value), 3) AS sample_mean
        FROM data USING SAMPLE 10% (bernoulli)
    """).df())
    # 100 行のリザーバ標本
    print(con.sql("""
        SELECT count(*) AS reservoir_n
        FROM (SELECT * FROM data USING SAMPLE 100 ROWS)
    """).df())

    print("\n=== approximate aggregates (近似集計) ===")
    print(con.sql("""
        SELECT
            approx_count_distinct(id) AS approx_distinct,
            count(DISTINCT id)        AS exact_distinct,
            round(approx_quantile(value, 0.5), 3) AS approx_median,
            round(quantile_cont(value, 0.5), 3)   AS exact_median
        FROM data
    """).df())

    print("\n=== bootstrap mean CI (反復標本で平均の信頼区間) ===")
    # 100 行のリザーバ標本を 200 回取り、平均の分布から 95% 区間を求める
    means = [con.sql("SELECT avg(value) FROM data USING SAMPLE 100 ROWS").fetchone()[0]
             for _ in range(200)]
    lo, hi = np.percentile(means, [2.5, 97.5])
    print("mean of sample means =", round(float(np.mean(means)), 3))
    print("95% CI =", (round(float(lo), 3), round(float(hi), 3)))


if __name__ == "__main__":
    main()
