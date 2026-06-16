# 05_sample05: 仮説検定（DuckDB → scipy）

SQL だけでは p 値の出る仮説検定は表現しづらいため、**集計・整形は DuckDB、検定は `scipy`** という役割分担を示すサンプルです。データはDBに置いたまま、必要な集計結果だけを取り出して検定します。

`sample1.py` の内容:
- グループ平均を DuckDB で算出（前処理）
- `list()` 集約でグループの値を取り出し、`scipy.stats.ttest_ind` で**二標本 t 検定**
- DuckDB でクロス集計し、`scipy.stats.chi2_contingency` で**カイ二乗検定**

このサンプルのみ `scipy` を使います（共通 `requirements.txt` に含まれています）。

## 実行
親フォルダ (`31_duckDB`) の共通 venv を有効化した状態で:
```bash
(env) $ python sample1.py
```
