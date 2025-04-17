import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import os
import mycolor

# 用于绘制雷达图（按四大区域划分）
# 使用方法：修改35行的point的值来绘制主粮作物/经济作物来绘制雷达图

provinces = [
    "北京市", "天津市", "河北省", "山西省", "内蒙古自治区",
    "辽宁省", "吉林省", "黑龙江省",
    "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",
    "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区",
    "海南省",
    "重庆市", "四川省", "贵州省", "云南省", "西藏自治区",
    "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区"
]

# 划分后的省份列表
east_provinces = ["北京市", "天津市", "河北省", "山东省","上海市" ,"江苏省", "浙江省", "福建省", "广东省", "海南省"]
central_provinces = ["山西省", "河南省", "安徽省", "湖北省", "湖南省", "江西省"]
west_provinces = ["内蒙古自治区", "陕西省", "甘肃省", "宁夏回族自治区", "青海省", "新疆维吾尔自治区", "四川省",
                  "重庆市", "贵州省", "云南省", "西藏自治区", "广西壮族自治区"]
northeast_provinces = ["辽宁省", "吉林省", "黑龙江省"]

# 将划分后的省份列表放入一个字典中
province_regions = {
    "东部地区": east_provinces,
    "中部地区": central_provinces,
    "西部地区": west_provinces,
    "东北部地区": northeast_provinces
}
# 修改point=主粮作物/经济作物来绘制雷达图
point='经济作物'

Maingrain_crops=['稻谷','小麦','玉米','大豆','高粱','马铃薯','大麦'] #主粮作物
cash_crop=['棉花','花生','油菜籽','芝麻','黄红麻','甘蔗','甜菜','烤烟','烟叶','药材'] #经济作物
crops_name=[]
crop_main={}

father_path="../dataset/"
savepath="../results/"


def cal(years, dict1):
    result={}
    for j in provinces:
        part1 = part2 = part3 = part4 = part5 = 0  # 我将公式分为了5个部分（只要是求和就分为一部分）
        cnt=1
        for i in range(len(years)):
            if np.isnan(dict1[j][i]):
                # 如果是NaN，则略过
                continue
            part1 += cnt * dict1[j][i]  # t从1开始，所以这里是i+1
            part2 += cnt
            part3 += dict1[j][i]
            part4 += cnt ** 2
            part5 += cnt
            cnt+=1

        if (cnt * part4 - part5 **2)==0:
            result[j]=0
        else:
            result[j] = (cnt * part1 - part2 * part3) / (cnt * part4 - part5 ** 2)

    tmp = [val for val in result.values()]
    flag = min(tmp)
    if flag < 0:
        for i in range(len(tmp)):
            tmp[i] += -flag
    tmp_sum = sum(tmp)

    for i in range(len(tmp)):
        tmp[i] /= tmp_sum

    for num, key in enumerate(result):
        result[key] = tmp[num]

    return result

def record_column(): #因为不同作物在不同表格中的行号不同，因此这个函数用于记录每个省中每个（主粮/经济）作物的行号，返回二维列表
    if point=='主粮作物':
        crop_list=Maingrain_crops
    else:
        crop_list=cash_crop

    croplst_sum=[[] for i in range(len(provinces))]
    for i in range(len(provinces)):  # 遍历所有省份
        data = pd.read_excel(father_path + provinces[i] + '.xlsx')  # 读取对应的文件
        data = np.array(data)
        for k in crop_list:#遍历所有作物
            for j in range(len(data)):#遍历文件所有行
                if data[j,0].startswith(k):
                    croplst_sum[i].append(j)
                    break

    return croplst_sum

def record_cropname():
    crop_sum=record_column()
    tmp=0 #作为crop_sum的下标，用于遍历crop_sum
    for cop in crop_sum[tmp]:
        flag = 0
        point = cop
        years = [i for i in range(2000, 2022)]
        dict1 = {}  # 用于保存  省份:占比
        for i in range(len(provinces)):  # 遍历所有省份
            data = pd.read_excel(father_path + provinces[i] + '.xlsx')  # 读取对应的文件
            data = np.array(data)  # 农作物总播种面积(千公顷)为第一行，粮食播种面积(公顷)为第二行，每行从第一列开始才是数据，所以下一行是range从1开始
            if not flag:
                s=data[point, 0]
                index_of_area = s.find('播种')

                crops_name.append(s[:index_of_area]+"增长率") # 作物名字
                flag = 1
            for j in range(1, len(data[0])):  # 因为农作物总播种面积(千公顷)和粮食播种面积(公顷)的尺度不一样，所以统一为(公顷)
                if not point == 8:  # 棉花的也是公顷
                    data[1][j] *= 1000

            dict1[provinces[i]] = np.flip(
                data[point, 1:] / data[1, 1:])  # flip的作用是翻转，因为年份是2000-2021，而文件中是2021-2000的顺序排列的，计算的value是粮食占农作物面积的比例

        result = cal(years, dict1)  # cal为核心计算函数，返回值是一个字典，key是各个省份的名称，对应的value是计算的斜率系数

        for i in range(len(provinces)):
            crop_main[provinces[i]].append(result[provinces[i]])
        tmp+=1

def leida(data,province,colork):
    data.append(data[0])

    # 计算雷达图中的角度
    num_vars = len(crops_name)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    angles += angles[:1]

    ax.plot(angles, data, label=province,color=colork)
    ax.fill(angles, data, alpha=0.25,color=colork)

    # 添加标签
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(crops_name, fontsize=15)

    # 添加图例
    plt.legend(prop={'size': 10}, ncol=1)


if __name__=='__main__':
    if os.path.exists(savepath) == False:
        os.makedirs(savepath)

    for province in provinces:
        crop_main[province] = []

    record_cropname()
    for key,value in crop_main.items():
        value=np.array(value)
        # 计算原始数据的均值和标准差
        mean_val = np.mean(value)
        std_val = np.std(value)

        # Z-Score标准化数据
        z_score_data = (value - mean_val) / std_val
        crop_main[key]=list(z_score_data)


    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    for key,value in province_regions.items():
        tmp=0
        # 绘制雷达图
        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
        for provience in value:
            leida(crop_main[provience], provience,mycolor.colors_normalized[tmp])
            tmp+=1
        plt.savefig(savepath + key +point+ '作物增长率雷达图归一化.png')
        plt.show()


