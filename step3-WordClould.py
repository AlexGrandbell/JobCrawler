#Created by AlexGrandbell on 2024/11/11
#本文件用于统计词频并创建词云（矩形）
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#读取清洗后的数据
data = pd.read_excel("cleaned_job_requirements.xlsx")
text_list = data['清理后的任职要求'].tolist()
#初始化TF-IDF向量器
tfidf_vectorizer = TfidfVectorizer(max_features=100)  #设定要提取的最大词数
tfidf_matrix = tfidf_vectorizer.fit_transform(text_list)
#获取词和对应的TF-IDF分数
tfidf_scores = dict(zip(tfidf_vectorizer.get_feature_names_out(), tfidf_matrix.sum(axis=0).A1))
#打印前40个高TF-IDF权重的词
print("前40个高TF-IDF权重的词:")
for word, score in sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:40]:
    print(f"{word}: {score:.4f}")

#创建词云
#配置词云对象
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    font_path="Hiragino Sans GB.ttc",
    max_words=100,
    colormap="viridis"
)

#生成词云
wordcloud.generate_from_frequencies(tfidf_scores)

#绘制词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()