import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import mycolor

father_path="../dataset/"
data_name="全国收入金额.xlsx"
savepath="../results/"
resultname="全国收入金额.png"
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

years=[str(i) for i in range(2000,2023)]
tmp = pd.read_excel(father_path + data_name)
tmp=np.array(tmp)

chengzhen=np.flip(tmp[0:23,-1]) #城镇居民人均可支配收入
nongcun=np.flip(tmp[24:47,-1]) #农村居民人均可支配收入
rate=chengzhen/nongcun  # 城乡收入倍差


n = len(years)
width = 0.3
index = np.arange(n)
fig, ax1 = plt.subplots(figsize=(18, 6))

# 绘制柱状图
ax1.bar(index, chengzhen, width, label='城镇居民人均可支配收入',color=mycolor.colors_normalized[0])
ax1.bar(index + width, nongcun, width, label='农村居民人均可支配收入',color=mycolor.colors_normalized[1])
# 设置x轴刻度
plt.xticks(index + width / 2, years)
ax1.set_xlabel('年份')
ax1.set_ylabel('元')
ax1.tick_params('y')
plt.legend(loc='upper left')

# 创建第二个y轴
ax2 = ax1.twinx()
# 绘制第二个y轴的数据
ax2.plot(years, rate, 'orange',label='城乡收入倍差(农村为1)',linewidth=1.5,color=mycolor.colors_normalized[2])
ax2.set_ylabel('倍')
ax2.tick_params('y')
plt.legend()

plt.savefig(os.path.join(savepath,resultname))

plt.show()





