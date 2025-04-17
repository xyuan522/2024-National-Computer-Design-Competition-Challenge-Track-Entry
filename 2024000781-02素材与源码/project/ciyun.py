# 导入文本需要的库需要的库
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import re
import pandas as pd
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 设置字体
# 读取生态环境部部长黄润秋新闻发布会
text = open("../dataset/2013.txt", encoding='utf-8').read()  # 标明文本路径
# 定义停用词列表
stopwords = ['和', '的', '是', '在', '有', '了', '我', '不', '人', '我们', '也', '都', '上', '一个', '很', '说', '到',
             '这个', '那', '你', '它', '他们', '自己', '着', '就', '还', '但', '会', '能', '要', '那么', '又', '看',
             '过', '把', '没', '下', '这些', '这样', '一些', '这个', '起来', '如果', '对于', '因为', '所以', '可能',
             '对', '再', '而且', '其实', '不过', '已经', '应该', '虽然', '只是', '只有', '很']

# 文本数据正则化函数
def text_cleaning(text):
    text = re.sub('\s+','', text)#remove whitespace
    text = re.sub('-|\.','', text)#remove '-','.'
    text = ' '.join([word for word in text if word not in stopwords])
    text = re.sub(r'Page\d', '', text)#remove "page" and gigit
    text = re.sub('[a-zA-Z]', '', text)#remove english
    return(text)
# 调用正则化函数
text = text_cleaning(text)
# jieba库词频提取
text = ' '.join(jieba.lcut(text))
# 设置词云背景图
image = Image.open("../dataset/leaf.png")
# 将图片转化为numpy数组格式
image = np.array(image)
# 生成词云对象
wc = WordCloud(font_path = '../dataset/SimHei.ttf', width = 3000, height = 1000, random_state = 50, background_color = 'White', mask = image).generate(text)

# 显示词云图
fig, ax1 = plt.subplots(figsize = (16, 7), dpi = 2000)
ax1.imshow(wc, interpolation = "bilinear")
# 不显示坐标轴
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
plt.axis("off")
# 保存词云图矢量格式
plt.savefig('../results/词云图2.png', dpi = 2000)
plt.show()
