import duckdb
import numpy as np
import pandas as pd


def make_data(seed=42):
    # 右に裾を引く（正の歪度を持つ）分布として指数分布を使う
    rng = np.random.default_rng(seed)
    n = 500
    return pd.DataFrame({
        "value": rng.exponential(scale=10.0, size=n).round(3),
    })


def main():
    df = make_data()
    con = duckdb.connect()
    con.register("data", df)

    print("=== quantiles & shape (分位点と分布の形) ===")
    query = """
        SELECT
            round(quantile_cont(value, 0.25), 3) AS q25,
            round(quantile_cont(value, 0.50), 3) AS median,
            round(quantile_cont(value, 0.75), 3) AS q75,
            round(quantile_cont(value, 0.75) - quantile_cont(value, 0.25), 3) AS iqr,
            round(approx_quantile(value, 0.50), 3) AS approx_median,
            round(skewness(value), 4) AS skewness,
            round(kurtosis(value), 4) AS kurtosis
        FROM data
    """
    print(con.sql(query).df())

    print("\n=== histogram (度数分布 / 幅 5 のビン) ===")
    # floor(value / 幅) でビン番号を作り、GROUP BY で度数を数える
    hist = """
        SELECT
            cast(floor(value / 5) AS INT)     AS bin,
            5 * cast(floor(value / 5) AS INT) AS lower_edge,
            count(*)                          AS freq
        FROM data
        GROUP BY bin
        ORDER BY bin
    """
    print(con.sql(hist).df())


if __name__ == "__main__":
    main()
