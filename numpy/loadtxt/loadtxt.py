import numpy as np

### データの読み込み
### 数値データがスペースで区切られたファイルの読み込み
### data という配列にデータが格納される
### data[0][0] は 1 行目 1 列目
FilePath = "./data.dat"
data = np.loadtxt(FilePath)

### 列ごとに分離することができる
column1 = data[:, 0]  ### 1列目
column2 = data[:, 1]  ### 2列目

### 最小値・最大値
min_column1 = np.min(column1)
min_column2 = np.min(column2)
max_column1 = np.max(column1)
max_column2 = np.max(column2)

print(f"column1 の範囲： {min_column1} ~ {max_column1}")
print(f"column2 の範囲： {min_column2} ~ {max_column2}")

