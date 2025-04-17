import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import mycolor

father_path="../dataset/"
data_name=".xlsx"
filelst=['城镇就业人员数','农村就业人员数','第一产业就业人口比重']
savepath="../results/"
resultname="全国乡村城镇就业年度变化情况.png"
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def drawpic(years, data):
    n = len(years)
    width = 0.35
    index = np.arange(n)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制柱状图
    ax1.bar(index, data[0], width, label='城镇就业人员数',color=mycolor.colors_normalized[0])
    ax1.bar(index + width, data[1], width, label='农村就业人员数',color=mycolor.colors_normalized[1])

    # 设置x轴刻度
    plt.xticks(index + width / 2, years)
    ax1.set_xlabel('年份')
    ax1.set_ylabel('万人')
    ax1.tick_params('y')
    plt.legend(loc='upper left')

    # 绘制折线图
    ax2 = ax1.twinx()
    ax2.plot(years, data[2], color=mycolor.colors_normalized[2], label='第一产业就业人口比重', marker='o')
    ax2.set_ylabel('%')
    ax2.tick_params('y')
    plt.legend(loc='upper right')

    plt.title('城镇与农村就业人员数及第一产业就业人口比重')
    plt.savefig(os.path.join(savepath,resultname))
    plt.show()

data=[]
years=[str(i) for i in range(2013,2023)]
for i in filelst:
    tmp = pd.read_excel(father_path +i+ data_name)
    tmp=np.array(tmp)
    data.append(np.flip(tmp[:-9,-1]))

drawpic(years,data)


