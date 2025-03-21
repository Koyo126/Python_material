import numpy as np
import matplotlib.pyplot as plt

### データの読み込み
ReadFilePath = "./data.dat"
data = np.loadtxt(ReadFilePath)

### 列ごとに分離することができる
column1 = data[:, 0]  ### 1列目
column2 = data[:, 1]  ### 2列目

### 最小値・最大値
min_column1 = np.min(column1)
min_column2 = np.min(column2)
max_column1 = np.max(column1)
max_column2 = np.max(column2)

### 分布の作成
bins = 1000  ### ビンの総数

### Usage : numpy.histgram
###   numpy.histogram(a, bins=100, range=None, normed=False, weights=None, density=None)
###     a --- ヒストグラムの元
###     bins --- int のときは階級の数。
###     density --- True  -> 総面積が 1 となるように規格化
###                 Flase -> ヒストグラム
hist_column1, bin_edges_column1 = np.histogram(column1, bins=bins, density=True)  ### density = True -> 分布にする
hist_column2, bin_edges_column2 = np.histogram(column2, bins=bins, density=True)

### ビンの中央を計算
bin_centers_column1 = (bin_edges_column1[:-1] + bin_edges_column1[1:]) /2.0
bin_centers_column2 = (bin_edges_column2[:-1] + bin_edges_column2[1:]) /2.0

### ファイルに保存
OutputDataPath = np.array(["column1.dat", "column2.dat"])

### Usage : numpy.savetxt
###   numpy.savetxt(fname, X, fmt=’%.18e’, delimiter=’ ‘, newline=’\n’, header=’’, footer=’’, comments=’#’, encoding=None)
###     fname --- 保存するファイル名。
###     X --- 保存データ
###     header --- ファイルの最初に書き込む string
###     comments --- headerやfooterを挿入する際、先頭に入力する文字を指定
np.savetxt(OutputDataPath[0], np.column_stack((bin_centers_column1, hist_column1)), header="# column1  \n#           x                    probability", comments="")
np.savetxt(OutputDataPath[1], np.column_stack((bin_centers_column2, hist_column2)), header="# column2  \n#           x                    probability", comments="")

### プロット
plt.figure(figsize=(8, 4.5))  ### (a. b) --- 横 a インチ、縦 b インチ
plt.plot(bin_centers_column1, hist_column1, label="column1", linewidth=3, linestyle="-")
plt.plot(bin_centers_column2, hist_column2, label="column2", linewidth=3, linestyle="--")
plt.tick_params(axis='both', labelsize=14)
plt.legend(fontsize=16)  
plt.tight_layout()  ### 各グラフ同士が重ならないように自動調整
plt.show()
