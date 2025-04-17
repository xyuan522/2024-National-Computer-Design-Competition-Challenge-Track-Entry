import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mycolor  # 自己定义的颜色文件，用于统一论文图片颜色

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
father_path="../dataset/"
data_name="汇总.xls"


def zoom(x, y, ax1, fg):
    """
    :param x: 要绘制的数据的x轴数据
    :param y: 要绘制的数据的y轴数据
    :param ax1: 原图，子图画在这个原图上
    :param fg: 用于控制绘制的颜色
    """
    zoombegin = 1  # 放大的区域开始于下标1
    zoomend = 5  # 放大的区域结束于下标1
    # 选择要放大的区域
    x_zoom = np.array(x[zoombegin:zoomend])
    y_zoom = np.array(y[zoombegin:zoomend])

    # 创建内嵌图的坐标轴
    box = ax1.get_position()

    ax2 = fig.add_axes([box.x0 + box.width * 0.6, box.y0 + box.height * 0.6,
                        box.width * 0.25, box.height * 0.25])  # 参数：开始x位置，开始y位置，图宽，图高

    # 绘制内嵌图
    ax2.plot(x_zoom, y_zoom, color=mycolor.colors_normalized[fg - 1], marker='p')
    ax2.set_xlabel('年份')
    ax2.set_ylabel('增长率变化量(%)')

    # 下面绘制的是子图中的增长幅度（线段上的星型）
    indices3 = [1, 2, 3]  # 要绘制的下标
    values3 = v_lst3[1:4]  # 要绘制的值

    for i in range(len(values3)):
        px = 0.5  # x轴偏移量，为了将星型画在线段的中点
        py = values3[i] / 2  # y轴偏移量
        ax2.plot(years[indices3[i]] + px, np.flip(lst3)[indices3[i]] + py, color=mycolor.colors_normalized[3],
                 marker='*',
                 markersize=10)
        text_label = f"{values3[i]:.2f}%"  # 格式化文本，保留两位小数
        # 添加文本标签，可以稍微偏移一些位置以避免重叠
        ax2.text(years[indices3[i]] + px, np.flip(lst3)[indices3[i]] + py, text_label, ha='center', va='bottom',
                 fontsize=8)

    # 设置内嵌图的坐标轴范围以匹配放大区域
    ax2.set_xlim(x_zoom.min() - 0.5, x_zoom.max() + 0.5)
    ax2.set_ylim(y_zoom.min() - 1, y_zoom.max() + 1)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()


data = pd.read_excel(father_path + data_name)
data = np.array(data)

lst1 = data[2, 2:] * 100  # 东部增长率
lst2 = data[5, 2:] * 100  # 西部增长率
lst3 = data[8, 2:] * 100  # 中部增长率

v_lst3 = []
for i in range(len(lst1) - 1):
    v_lst3.append((np.flip(lst3)[i + 1] - np.flip(lst3)[i]))

sum_lst = []  # 汇总所有值，用于确定图表的边界
sum_lst.extend(lst1)
sum_lst.extend(lst2)
sum_lst.extend(lst3)

years = [i for i in range(2004, 2013)]
fig, ax = plt.subplots(figsize=(10, 6))
# 绘制中部地区的乡村人口增长率
ax.plot(years, np.flip(lst1), label='东部增长率', color=mycolor.colors_normalized[0], marker='o')

# 绘制东部地区的乡村人口增长率
ax.plot(years, np.flip(lst2), label='西部增长率', color=mycolor.colors_normalized[1], marker='s')

# 绘制西部地区的乡村人口增长率
ax.plot(years, np.flip(lst3), label='中部增长率', color=mycolor.colors_normalized[2], marker='^')

# 设置图表坐标轴标签
ax.set_xlabel('年份')
ax.set_ylabel('劳动力人口增长率(%)')

# 设置网格
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.xlim(years[0] - 0.5, years[-1] + 0.5)
plt.xticks(range(years[0], years[-1] + 1, 1))
plt.ylim(min(sum_lst) - 1, max(sum_lst) + 0.5)
plt.yticks(range(int(min(sum_lst)), int(max(sum_lst)) + 2, 2))

# 自动调整子图参数，使之填充整个图像区域且避免重叠
plt.tight_layout()

# 绘制放大的小图，fg的值与lst的值相对应，比如fg=3，那么lst3。fg用于同步大图与小图线的颜色
zoom(years, np.flip(lst3), ax, fg=3)

# 显示图例
ax.legend()

plt.savefig("../results/各区域乡村劳动力增长率.png")

# 显示图表
plt.show()
