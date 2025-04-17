from pyecharts.charts import WordCloud
from jieba import analyse

# 基于TextRank算法从文本中提取关键词
text_rank = analyse.textrank
text = open('../dataset/2023.txt', 'r', encoding='utf-8').read()
keywords = text_rank(text)
print(keywords)

text_list = []
# 输出提取的关键词
for keyword, weight in text_rank(text, withWeight=True):
    print('%s %s' % (keyword, weight))
    text_list.append((keyword, weight))

word_cloud = WordCloud()
# SHAPES = ("cardioid", "diamond", "triangle-forward", "triangle", "pentagon", "star")
word_cloud.add(series_name='热点分析', data_pair=text_list, word_size_range=[15,90], shape='cardioid', height=600,width=800)
# word_cloud.render('word_clound4.html')

