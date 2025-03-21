import glob

### ワイルドカードを用いてファイルを検索
files = glob.glob("test*.dat")

### 見つかったファイルを表示
for file in files:
  print(f"見つかったファイル: {file}")
