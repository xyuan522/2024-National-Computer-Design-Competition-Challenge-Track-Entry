import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mycolor
import os

father_path="../dataset/"
data_name="全国农民工规模.xlsx"
savepath="../results/"
resultname="全国农民工规模.png"
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

years=[str(i) for i in range(2008,2023)]
tmp = pd.read_excel(father_path + data_name)
tmp=np.array(tmp)

local_labor=np.flip(tmp[0:15,-1]) # 本地农民工数
labor=np.flip(tmp[16:31,-1]) # 外出农民工
waichu_labor=np.flip(tmp[32:47,-1]) # 外出农民工数
wage=np.flip(tmp[48:63,-1]) # 月均收入

n = len(years)
width = 0.3
index = np.arange(n)
fig, ax1 = plt.subplots(figsize=(18, 6))

# 绘制柱状图
ax1.bar(index, labor, width, label='农民工人数',color=mycolor.colors_normalized[0])
ax1.bar(index + width, waichu_labor, width, label='外出农民工占比',color=mycolor.colors_normalized[1])
ax1.bar(index + 2*width, local_labor, width, label='本地农民工占比',color=mycolor.colors_normalized[2])
# 设置x轴刻度
plt.xticks(index + 2*width / 2, years)
ax1.set_xlabel('年份')
ax1.set_ylabel('万人')
ax1.tick_params('y')
plt.legend(loc='upper left')

# 创建第二个y轴
ax2 = ax1.twinx()

# 绘制第二个y轴的数据
ax2.plot(years, wage, color=mycolor.colors_normalized[3],label='月均收入',linewidth=2.5,marker='s')
ax2.set_ylabel('元/人')
ax2.tick_params('y')
plt.legend()

plt.savefig(os.path.join(savepath,resultname))

plt.show()





