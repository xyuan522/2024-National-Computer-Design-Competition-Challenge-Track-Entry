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

#修改data中的值来绘制，文章中图片里面作物的划分在列表中用空行分开了
data = [
    ["粮食产量(万吨)",
    "稻谷产量(万吨)",
    "小麦产量(万吨)",
    "玉米产量(万吨)",
    "薯类产量(万吨)"],

    ["农作物总播种面积(千公顷)",
    "粮食作物播种面积(千公顷)",
     "稻谷播种面积(千公顷)",
    "小麦播种面积(千公顷)",
    "玉米播种面积(千公顷)",
    "薯类播种面积(千公顷)"]
]

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
savepath="results"

father_path="../dataset/"
data_name="chinese_grains_product2.csv"
oridata = pd.read_csv(father_path+data_name)
plt.figure(figsize=(12, 6))


items=1#可取值有0,1,2。分别代表data中的不同列表
if items==0:
    item_name="产量(万吨)"
else:
    item_name="播种面积(千公顷)"
resultname=str(items)+".png"
data_items=data[items]
local_color=mycolor.colors_normalized[:]
if items==0:
    local_color[0],local_color[2]=local_color[2],local_color[0]
    local_color[0], local_color[3] = local_color[3], local_color[0]
elif items==2:# 为了使得同一趋势的线绘制出来色系相似
    local_color[2] = local_color[3]
    local_color[3]=local_color[4]

color_pt=0

# 创建主图
fig, ax1 = plt.subplots(figsize=(12, 8))
ax_point=ax1
is_first=2
lines=labels=None
for name in data_items:

    data = oridata[:]
    time_series = data[name]
    time_series.index = pd.RangeIndex(start=1949, stop=2023, step=1)

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
            ax_point.plot(time_series, label=name + '实际数据', color=local_color[color_pt])
            # 注意这里需要调整x轴的范围以匹配预测的长度
            ax_point.plot(forecast_series, label=name + '预测数据', color=local_color[color_pt], linestyle='--',
                          linewidth=3)
            ax_point.set_xlabel("年份")
            if items == 1 and is_first>0:
                ax_point.set_ylabel("农作物与粮食"+item_name)
                is_first-=1
            elif items==0:
                ax_point.set_ylabel(item_name)

            if items == 1 and is_first==0:
                lines, labels = ax_point.get_legend_handles_labels()
                # 创建第二个y轴
                ax2 = ax1.twinx()
                ax_point = ax2
                ax_point.set_ylabel("其他"+item_name)
                is_first-=1
        else:
            print("差分后的序列仍然不是平稳的，可能需要进一步处理或选择其他模型。")
    else:
        print("原始时间序列已经是平稳的，可以直接拟合模型。")
        model = SARIMAX(time_series, order=(1, 0, 1), seasonal_order=(1, 0, 1, 12))
        results = model.fit()

        # 预测差分序列
        forecast = results.predict(start=len(time_series), end=len(time_series) + 11)

        # 创建年份索引，从2023年到2034年
        years = pd.RangeIndex(start=2023, stop=2036, step=1)  # 注意：stop是2035，因为RangeIndex是左闭右开的

        # 使用给定的值和年份索引创建新的Series
        forecast_series = pd.Series(forecast, index=years)

        # 可视化结果
        ax_point.plot(time_series, label=name + '实际数据', color=local_color[color_pt])
        # 注意这里需要调整x轴的范围以匹配预测的长度
        ax_point.plot(forecast_series, label=name + '预测数据', color=local_color[color_pt], linestyle='--',
                      linewidth=3)
        ax_point.set_xlabel("年份")
        if items == 1 and is_first > 0:
            ax_point.set_ylabel("农作物与粮食" + item_name)
            is_first -= 1
        elif items == 0:
            ax_point.set_ylabel(item_name)

        if items == 1 and is_first == 0:
            lines, labels = ax_point.get_legend_handles_labels()
            # 创建第二个y轴
            ax2 = ax1.twinx()
            ax_point = ax2
            ax_point.set_ylabel("其他" + item_name)
            is_first -= 1
    color_pt+=1

if items==1:
    lines2, labels2 = ax_point.get_legend_handles_labels()
    # 合并线条和标签
    lines += lines2
    labels += labels2

    # 创建一个新的图例（可以放在任何位置，这里我们放在图形的右下角）
    plt.legend(lines, labels, loc='upper left',prop={'size': 8}, ncol=2)
else:
    plt.legend()
plt.savefig(savepath + resultname)
plt.show()