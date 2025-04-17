import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mycolor
import os

father_path="../dataset/"
data_name="指标数据.xlsx"
savepath="../results/"
resultname="全国主要年份的农村劳动力转移率变化趋势.png"
rate=0.7  # 农村劳动力人口大约占农村总人口的70%
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data=pd.read_excel(father_path+data_name)

data=np.array(data)

# data的第0行为年份，从2021——1990,第1行为乡村人口数(万人),第2行为乡村人口占总人口比重(%),第3行为乡村就业人员数(年末)(万人),第4行为第一产业就业人员数(年末)(万人)

years=[i for i in range(1990,2022)]
# lst代表劳动力转移率。劳动力转移率=(劳动力人口-第一产业就业人员数)/劳动力人口。劳动力人口=乡村人口数*0.7
lst=np.flip((data[1,1:]*rate-data[4,1:])/(data[1,1:]*rate)) # 因为数据是从2021——1990的，但是画图要从1990——2021，所以使用flip翻转一下
# lst2代表环比增长率。环比增长率=(第i年的劳动力转移率-第i-1年的劳动力转移率)/第i-1年的劳动力转移率
lst2=[]
for i in range(1,len(lst)):
    lst2.append((lst[i]-lst[i-1])/lst[i-1])

# 创建主图
fig, ax1 = plt.subplots(figsize=(8, 6))

# 绘制第一个y轴的数据
ax1.plot(years, lst, color=mycolor.colors_normalized[0],marker='s',label='劳动力转移率')
print(len(years))
print(len(lst))
ax1.set_xlabel('年份')
ax1.set_ylabel('劳动力转移率')
ax1.tick_params('y')
plt.legend()

# 创建第二个y轴
ax2 = ax1.twinx()

# 绘制第二个y轴的数据
ax2.plot(years[1:], lst2, color=mycolor.colors_normalized[1],label='环比增长率',linewidth=1.5)
print(len(lst2))
ax2.set_ylabel('环比增长率')
ax2.tick_params('y')
plt.legend()

plt.savefig(os.path.join(savepath,resultname))

plt.show()