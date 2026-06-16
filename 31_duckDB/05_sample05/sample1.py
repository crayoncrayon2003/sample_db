import duckdb
import numpy as np
import pandas as pd
from scipy import stats


def make_data(seed=21):
    # グループ B の平均をやや高くして、t 検定で差が出やすくする
    rng = np.random.default_rng(seed)
    n = 100
    a = rng.normal(50, 10, n)
    b = rng.normal(54, 10, n)
    return pd.DataFrame({
        "grp": ["A"] * n + ["B"] * n,
        "value": np.concatenate([a, b]),
        "category": rng.choice(["X", "Y", "Z"], size=2 * n),
    })


def main():
    df = make_data()
    con = duckdb.connect()
    con.register("data", df)

    # SQL では平均差までは出せても p 値が出せない。
    # 集計・整形は DuckDB で行い、検定だけ scipy に渡す。
    print("=== group means in DuckDB (前処理) ===")
    print(con.sql("""
        SELECT grp, count(*) AS n, round(avg(value), 3) AS mean
        FROM data GROUP BY grp ORDER BY grp
    """).df())

    print("\n=== two-sample t-test (A vs B) via scipy ===")
    rows = con.sql("SELECT grp, list(value) AS vals FROM data GROUP BY grp ORDER BY grp").fetchall()
    groups = {grp: np.array(vals) for grp, vals in rows}
    t, p = stats.ttest_ind(groups["A"], groups["B"])
    print("t =", round(float(t), 4), " p =", round(float(p), 4))

    print("\n=== chi-square test (grp x category) via scipy ===")
    # DuckDB でクロス集計してから検定する
    ct = con.sql("""
        SELECT grp, category, count(*) AS n
        FROM data GROUP BY grp, category
    """).df()
    table = ct.pivot(index="grp", columns="category", values="n").fillna(0).values
    chi2, p2, dof, _ = stats.chi2_contingency(table)
    print("chi2 =", round(float(chi2), 4), " p =", round(float(p2), 4), " dof =", dof)


if __name__ == "__main__":
    main()
