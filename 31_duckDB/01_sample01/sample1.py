import duckdb
import numpy as np
import pandas as pd


def make_data(seed=42):
    # シード固定で再現可能なデータを生成する
    rng = np.random.default_rng(seed)
    n = 200
    return pd.DataFrame({
        "grp": rng.choice(["A", "B"], size=n),
        "value": rng.normal(loc=50, scale=10, size=n).round(2),
    })


def main():
    df = make_data()
    con = duckdb.connect()
    con.register("data", df)

    print("=== SUMMARIZE (列ごとの自動要約) ===")
    print(con.sql("SUMMARIZE SELECT * FROM data").df())

    print("\n=== descriptive statistics (記述統計) ===")
    query = """
        SELECT
            count(*)                       AS n,
            round(avg(value), 3)           AS mean,
            round(median(value), 3)        AS median,
            round(stddev_samp(value), 3)   AS sd,
            round(var_samp(value), 3)      AS variance,
            min(value)                     AS min,
            max(value)                     AS max,
            round(mad(value), 3)           AS mad
        FROM data
    """
    print(con.sql(query).df())

    print("\n=== per group (グループ別) ===")
    query_grp = """
        SELECT grp,
               count(*)                     AS n,
               round(avg(value), 3)         AS mean,
               round(stddev_samp(value), 3) AS sd
        FROM data
        GROUP BY grp
        ORDER BY grp
    """
    print(con.sql(query_grp).df())


if __name__ == "__main__":
    main()
