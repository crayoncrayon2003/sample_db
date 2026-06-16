import duckdb
import numpy as np
import pandas as pd


def make_data(seed=7):
    # y は x と強く相関させ、z は独立にする
    rng = np.random.default_rng(seed)
    n = 200
    x = rng.normal(0, 1, n)
    y = 2.0 * x + rng.normal(0, 0.5, n)
    z = rng.normal(0, 1, n)
    return pd.DataFrame({"x": x, "y": y, "z": z})


def main():
    df = make_data()
    con = duckdb.connect()
    con.register("data", df)

    print("=== correlation & covariance (相関・共分散) ===")
    query = """
        SELECT
            round(corr(x, y), 4)        AS corr_xy,
            round(corr(x, z), 4)        AS corr_xz,
            round(covar_samp(x, y), 4)  AS cov_xy,
            round(covar_pop(x, y), 4)   AS covpop_xy
        FROM data
    """
    print(con.sql(query).df())

    print("\n=== correlation matrix (相関行列) ===")
    matrix = """
        SELECT 'x' AS var, round(corr(x, x), 3) AS x, round(corr(x, y), 3) AS y, round(corr(x, z), 3) AS z FROM data
        UNION ALL
        SELECT 'y',        round(corr(y, x), 3),      round(corr(y, y), 3),      round(corr(y, z), 3)      FROM data
        UNION ALL
        SELECT 'z',        round(corr(z, x), 3),      round(corr(z, y), 3),      round(corr(z, z), 3)      FROM data
    """
    print(con.sql(matrix).df())


if __name__ == "__main__":
    main()
