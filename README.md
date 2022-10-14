# 出欠とるとる君

慶應義塾大学SFC 情報基礎の出欠を取るべく、受講者の名前をひたすら読み上げてくれます  
欠席者の集計もしてくれます。

## 使い方

### 0. 環境構築

```
pipenv install
```

### 1. 名簿CSVを以下の形式で作成する

```csv
竹村 太希,ﾀｹﾑﾗ ﾋﾛｷ
佐藤 太郎,ｻﾄｳ ﾀﾛｳ
John McCarthy,ｼﾞｮﾝ ﾏｯｶｰｼｰ
```

### 2. 実行

```sh
pipenv run python main.py [CSVファイルのパス]
```
