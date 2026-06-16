# 06_sample06: ウィンドウ関数・グループ統計

DuckDB のウィンドウ関数とグループ集計で、順位付け・移動平均・小計を求めるサンプルです。
10 日 × 2 地域の売上データを使います。

`sample1.py` の内容:
- `rank()` / `ntile(4)` / `percent_rank()`（地域内の順位・四分位・相対順位）
- ウィンドウフレーム `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` による 3 期移動平均
- `GROUP BY ROLLUP(...)` で地域別＋総計の小計

## 実行
親フォルダ (`31_duckDB`) の共通 venv を有効化した状態で:
```bash
(env) $ python sample1.py
```
