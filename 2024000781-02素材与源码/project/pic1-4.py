import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mycolor

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

education_levels = {
    "低等教育": ["未上过学", "扫   盲   班"],
    "基础教育": ["小      学", "初      中"],
    "高中教育": ["高      中"],
    "职业教育": ["中      专", "大学专科"],
    "高等教育": ["大学本科", "研   究   生"]
}

p_year="2020"

father_path="../dataset/"
data_name=p_year+".xls"
savepath="../results/"
resultname=p_year+"年按年龄、性别和教育程度分列的人口金字塔.png"

data_new_loaded = pd.read_excel(father_path+data_name)

# 初始化存储计算结果的字典
calculated_data = {}

# 遍历每个教育水平，分别计算男女人数总和
for level, cols in education_levels.items():
    male_sum = pd.Series([0] * len(data_new_loaded.iloc[1:, 0]))
    female_sum = pd.Series([0] * len(data_new_loaded.iloc[1:, 0]))
    for col in cols:
        male_index = data_new_loaded.columns.get_loc(col)
        female_index = male_index + 1  # 假设女性列紧跟在男性列后面
        male_sum += pd.to_numeric(data_new_loaded.iloc[1:, male_index], errors='coerce').fillna(0)
        female_sum += pd.to_numeric(data_new_loaded.iloc[1:, female_index], errors='coerce').fillna(0)
    calculated_data[level] = {"male": -male_sum, "female": female_sum}  # 男性人数取负值以便在图表中显示在左侧

# 绘制图表
fig, ax = plt.subplots(figsize=(10, 8))
age_labels = data_new_loaded.iloc[1:, 0].tolist()
colors = [mycolor.colors_normalized[3]]+mycolor.colors_normalized[6:]
level_order = ["低等教育","基础教育","高中教育","职业教育","高等教育"]

male_bottom = pd.Series([0] * len(age_labels))
female_bottom = pd.Series([0] * len(age_labels))

for i, level in enumerate(level_order):
    if calculated_data[level]["male"] is None:
        continue
    ax.barh(age_labels, calculated_data[level]["male"], color=colors[i],
            left=male_bottom, label=level.replace("_", " ").title())
    ax.barh(age_labels, calculated_data[level]["female"], color=colors[i], left=female_bottom)
    male_bottom += calculated_data[level]["male"]
    female_bottom += calculated_data[level]["female"]
    male_bottom = male_bottom.fillna(0)
    female_bottom = female_bottom.fillna(0)
# 添加一条垂直线于中间，用于区分男性和女性
ax.axvline(x=0, color='black', lw=1)

# 显示更明显的网格线
ax.grid(True, which='both', linestyle='-', linewidth=0.5)

ax.set_xlabel('人数')
ax.set_ylabel('年龄')

# 获取x轴当前的tick locations和labels
x_ticks, x_labels = ax.get_xticks(), ax.get_xticklabels()

# 自定义新的x轴标签，对于负值取绝对值
new_x_labels = [abs(tick) if tick < 0 else tick for tick in x_ticks]

x_position=3800000 if p_year=="2000" else 2500000
y_position=0.3

# 在x轴正半轴附近添加文本“女性”
ax.text(x_position, y_position, '女性人数', ha='center', va='center', fontsize=12)

# 在x轴负半轴附近添加文本“男性”
ax.text(-x_position, y_position, '男性人数', ha='center', va='center', fontsize=12)

# 设置新的x轴标签
ax.set_xticklabels(new_x_labels)

ax.legend()
plt.savefig(savepath+resultname)

plt.show()