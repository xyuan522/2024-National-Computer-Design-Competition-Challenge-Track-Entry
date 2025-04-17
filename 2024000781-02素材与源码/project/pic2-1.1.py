import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller
import mycolor

def is_stationary(time_series):
    result = adfuller(time_series)
    # 判断是否平稳
    is_stat = result[1] < 0.05  # 通常使用0.05作为显著性水平
    print('Is the series stationary? ', is_stat)
    return is_stat
#修改data_items中的值来绘制，文章中图片里面作物的划分在列表中用空行分开了
data = [
    ["棉花播种面积(千公顷)",
    "甜菜播种面积(千公顷)",
    "油料播种面积(千公顷)",
    "蔬菜播种面积(千公顷)"],

    ["蔬菜产量(万吨)",
    "棉花产量(万吨)",
    "油料产量(万吨)",
    "甜菜产量(万吨)"]
]


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
father_path="../dataset/"
data_name="chinese_ecograins_area.xls"
oridata = pd.read_excel(father_path+data_name)
plt.figure(figsize=(12, 6))

items=0#可取值有0,1。分别代表data中的不同列表
if items==0:
    item_name="播种面积(千公顷)"
else:
    item_name="产量(万吨)"
resultname=str(items)+"eco.png"
data_items=data[items]
color_pt=0

local_color=mycolor.colors_normalized[:]
if items==0:
    pass
elif items==1:# 为了使得同一趋势的线绘制出来色系相似
    local_color[0],local_color[3] = local_color[3],local_color[0]

# 创建主图
fig, ax1 = plt.subplots(figsize=(12, 8))
ax_point=ax1
is_first=1
lines=labels=None

for name in data_items:
    s_begin=1990
    data = oridata[:]
    if name =="蔬菜产量(万吨)":
        s_begin=1995
        time_series=data[name][5:]
    else:
        time_series = data[name]

    time_series.index = pd.RangeIndex(start=s_begin, stop=2023, step=1)

    # 检查原始时间序列的平稳性
    if not is_stationary(time_series):
        diff_series = time_series.diff(1)
        diff_series = diff_series.dropna()

        # 检查差分后序列的平稳性
        if is_stationary(diff_series):
            # 使用差分序列拟合模型
            model = SARIMAX(diff_series, order=(1, 0, 1), seasonal_order=(1, 0, 1, 12))
            results = model.fit()

            # 预测差分序列
            forecast_diff = results.predict(start=len(diff_series), end=len(diff_series) + 11)

            # 检查 forecast_diff 是否包含 nan 值
            if np.isnan(forecast_diff).any():
                raise ValueError("差分序列的预测中包含 NaN 值。")

            # 将差分预测转换回原始序列尺度
            time_series = time_series.dropna()
            last_observed = time_series.iloc[-1]
            if np.isnan(last_observed):
                raise ValueError("最后一个观察值是 NaN。")

            # 确保 forecast_original_scale 不包含 NaN 值
            forecast_original_scale = np.append([last_observed], forecast_diff)

            # 计算累积和
            forecast = np.cumsum(forecast_original_scale)

            # 再次检查 forecast 是否包含 nan 值
            if np.isnan(forecast).any():
                raise ValueError("转换后的预测序列中包含 NaN 值。")

            # 创建年份索引，从2023年到2034年
            years = pd.RangeIndex(start=2022, stop=2035, step=1)  # 注意：stop是2035，因为RangeIndex是左闭右开的

            # 使用给定的值和年份索引创建新的Series
            forecast_series = pd.Series(forecast, index=years)

            # 可视化结果

            ax_point.plot(time_series, label=name+'实际数据', color=local_color[color_pt])
            # 注意这里需要调整x轴的范围以匹配预测的长度
            ax_point.plot(forecast_series, label=name+'预测数据', color=local_color[color_pt],linestyle='--',linewidth=3)
            ax_point.set_xlabel("年份")
            if items==1 and is_first:
                ax_point.set_ylabel("蔬菜"+item_name)
                lines,labels = ax_point.get_legend_handles_labels()
                is_first=0
                # 创建第二个y轴
                ax2 = ax1.twinx()
                ax_point=ax2
            elif items==1:
                ax_point.set_ylabel("其他"+item_name)
            else:
                ax_point.set_ylabel(item_name)

        else:
            print("差分后的序列仍然不是平稳的，可能需要进一步处理或选择其他模型。")
    else:
        print("原始时间序列已经是平稳的，可以直接拟合模型。")
    color_pt+=1

if items==1:
    lines2, labels2 = ax_point.get_legend_handles_labels()
    # 合并线条和标签
    lines += lines2
    labels += labels2

    # 创建一个新的图例（可以放在任何位置，这里我们放在图形的右下角）
    plt.legend(lines, labels, loc='upper left')
else:
    plt.legend()
# plt.savefig(savepath + resultname)
plt.show()