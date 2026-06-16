# 07_sample07: サンプリング・近似集計

大規模データ向けに、標本抽出（サンプリング）と近似集計を DuckDB で行うサンプルです。
1 万件のデータを使います。

`sample1.py` の内容:
- `USING SAMPLE 10%`（ベルヌーイ標本）、`USING SAMPLE 100 ROWS`（リザーバ標本）
- `approx_count_distinct`（近似ユニーク数）と厳密値の比較
- `approx_quantile` と `quantile_cont`（厳密分位点）の比較
- リザーバ標本を反復取得し、平均のブートストラップ 95% 信頼区間を推定

## 実行
親フォルダ (`31_duckDB`) の共通 venv を有効化した状態で:
```bash
(env) $ python sample1.py
```
