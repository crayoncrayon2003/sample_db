# 00_sample00: DuckDB 基礎

DuckDB の基本的な使い方のサンプルです。

- `sample1_DBpath.py` … 永続DB（`database.duckdb`）に接続し、CSV / JSON を取り込んで SQL で変換・保存・読み出し
- `sample2_memory.py` … インメモリDB（`:memory:`）で同様の処理

データは `data.csv` / `data.json`、変換用クエリは `query_duck.sql` を使います。

## 準備
仮想環境は親フォルダ (`31_duckDB`) の共通 venv を使います。未作成なら親の `README.md` を参照してください。

```bash
# 親フォルダで venv を有効化済みの状態で
(env) $ cd 00_sample00
```

## Test
```bash
(env) $ python sample1_DBpath.py
(env) $ python sample2_memory.py
```

実行すると `database.duckdb` や `output_*.json` が生成されます（`.gitignore` 済み）。
