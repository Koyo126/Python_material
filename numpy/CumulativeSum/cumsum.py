import numpy as np
import matplotlib.pyplot as plt

### データファイルの読み込み
ReadFilePath = 'data.dat'
data = np.loadtxt(ReadFilePath)

### x_min, x_max, data の列を取り出す
x_min = data[:, 0]
x_max = data[:, 1]
dA = data[:, 2]

### 積分 (累積和)
### [1, 2, 3] -> cumsum -> [1, 3, 6]
F = np.cumsum(dA)
F -= F[-1]  ### 最後の値を引いて基準を調整

### F の結果をファイルに出力
OutputFilePath = 'output.dat'

### x_max と F を一緒に保存する
np.savetxt(OutputFilePath, np.column_stack((x_max, F)), header="r  F", fmt='%.6f')


### プロット
plt.plot(x_max, F, marker='o', linestyle='-', color='b')
plt.xlabel('x')
plt.ylabel('y')
plt.title('cumulative sum')
plt.grid(False)
plt.show()

