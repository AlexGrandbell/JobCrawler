#Created by AlexGrandbell on 2024/11/11
#本文件用于统计词频并创建词云（图片形状）
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np

#读取清洗后的数据
data = pd.read_excel("cleaned_job_requirements.xlsx")
text_list = data['清理后的任职要求'].tolist()
#初始化TF-IDF向量器
tfidf_vectorizer = TfidfVectorizer(max_features=100)  #设定要提取的最大词数
tfidf_matrix = tfidf_vectorizer.fit_transform(text_list)
#获取词和对应的TF-IDF分数
tfidf_scores = dict(zip(tfidf_vectorizer.get_feature_names_out(), tfidf_matrix.sum(axis=0).A1))
#打印前50个高TF-IDF权重的词
print("50个高TF-IDF权重的词:")
for word, score in sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:50]:
    print(f"{word}: {score:.4f}")

#创建词云
#读取形状图像并转化为数组
mask = np.array(Image.open("head.png"))#这里换成图片名称

#创建词云对象，使用形状图像作为mask
wordcloud = WordCloud(
    width=800,
    height=400,
    font_path="Hiragino Sans GB.ttc",
    background_color="white",
    mask=mask,
    max_words=100,
    #contour_width=1,
    contour_color="steelblue"
)

#根据词频数据生成词云
wordcloud.generate_from_frequencies(tfidf_scores)

#显示词云
plt.figure(figsize=(8,8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()