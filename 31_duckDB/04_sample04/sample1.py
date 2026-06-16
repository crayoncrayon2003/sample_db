import duckdb
import numpy as np
import pandas as pd


def make_data(seed=3):
    # y = 3*x + 5 + ノイズ。最小二乗で slope≈3, intercept≈5 を復元できるはず
    rng = np.random.default_rng(seed)
    n = 200
    x = rng.uniform(0, 10, n)
    y = 3.0 * x + 5.0 + rng.normal(0, 2.0, n)
    return pd.DataFrame({"x": x, "y": y})


def main():
    df = make_data()
    con = duckdb.connect()
    con.register("data", df)

    print("=== linear regression by SQL (最小二乗・単回帰) ===")
    query = """
        SELECT
            round(regr_slope(y, x), 4)     AS slope,
            round(regr_intercept(y, x), 4) AS intercept,
            round(regr_r2(y, x), 4)        AS r2,
            round(regr_avgx(y, x), 4)      AS avg_x,
            round(regr_avgy(y, x), 4)      AS avg_y,
            regr_count(y, x)               AS n
        FROM data
    """
    print(con.sql(query).df())

    print("\n=== prediction (回帰式で予測) ===")
    # DuckDB 内で求めた係数を使って新しい x を予測する
    pred = """
        WITH model AS (
            SELECT regr_slope(y, x) AS b1, regr_intercept(y, x) AS b0 FROM data
        )
        SELECT t.nx AS x, round(model.b0 + model.b1 * t.nx, 3) AS y_pred
        FROM model, (VALUES (0.0), (2.5), (5.0), (7.5), (10.0)) AS t(nx)
        ORDER BY t.nx
    """
    print(con.sql(pred).df())


if __name__ == "__main__":
    main()
