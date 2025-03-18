#########################################################################
###
### sin(x) をプロットする
###
#########################################################################

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10.0, 10.0, 0.1)  ### -10 から 10 の範囲で 0.1 刻みでの配列を作る
y = np.sin(x)  ### 配列 x の値に対して sin(x) の配列を作る

### 図のサイズを変更
### 横 a インチ、縦 b インチに設定 --- figsize(a, b)
plt.figure(figsize=(8, 5.0))

### プロットするものを指定
plt.plot(x, y, linewidth=3, linestyle="-", label="sin(x)")  

### 軸ラベルの設定
plt.xlabel("x", fontsize=16)  ### x 軸のラベル
plt.ylabel("y", fontsize=16)  ### y 軸のラベル

### 軸の目盛の数字のサイズ
plt.tick_params(axis="both", labelsize=16)  ### "both" --- x 軸と y 軸に適用

### 凡例の設定
plt.legend(fontsize=16)

plt.show()  ### 図を表示

