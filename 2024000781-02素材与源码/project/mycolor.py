import matplotlib.pyplot as plt
import numpy as np

# 定义RGB颜色值列表
colors = [
    (99, 178, 238), (118, 218, 145), (248, 203, 127),
    (248, 149, 136), (124, 214, 207), (145, 146, 171),
    (120, 152, 225), (239, 166, 102), (237, 221, 134),
    (153, 135, 206), (99, 178, 238), (118, 218, 145)
]

# 将RGB颜色值转换为matplotlib可以理解的格式
colors_normalized = [(r / 255, g / 255, b / 255) for r, g, b in colors]

def showcolor():
    # 创建柱状图的索引
    indices = np.arange(len(colors))

    # 绘制柱状图，设置柱状图的宽度和颜色
    width = 0.35  # 可以根据需要调整宽度
    plt.bar(indices, [1] * len(colors), width, color=colors_normalized)

    # 设置图表标题和坐标轴标签
    plt.title('RGB Color Values as Bar Chart')
    plt.xlabel('Color Index')
    plt.ylabel('Value')

    # 移除y轴刻度（因为所有值都是1，所以不需要刻度）
    plt.yticks([])

    # 调整x轴刻度标签，使其居中
    plt.xticks(indices, [f'RGB({c[0]}, {c[1]}, {c[2]})' for c in colors])

    # 显示图表
    plt.show()

# showcolor()