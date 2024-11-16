# Created by AlexGrandbell on 2024/11/11
#本文件用于处理爬取到的职位信息
import pandas as pd
import jieba
import re

#读取数据
job_df = pd.read_excel("job_requirements.xlsx")

#加载停用词表
with open("stop_words.txt", "r", encoding="utf-8") as f:
    stop_words = set(f.read().splitlines())

def clean_text(text):
    #分词
    words = jieba.cut(text)

    #去除停用词、无意义数字和长串字母
    clean_words = []
    for word in words:
        #去除停用词
        if word in stop_words:
            continue
        #如果是数字或者无意义的长英文单词，跳过
        if re.match(r'^\d+$', word):  #如果是数字
            continue
        #保留中文字符和英文单词，去除其他符号
        word = re.sub(r'[^\u4e00-\u9fa5A-Za-z]', '', word)
        if word:  #只保留非空词汇
            clean_words.append(word)

    return " ".join(clean_words)


#对每条数据进行处理
job_df['清理后的任职要求'] = job_df['任职要求'].apply(clean_text)

#保存处理后的数据
job_df[['职位名称', '链接', '清理后的任职要求']].to_excel("cleaned_job_requirements.xlsx", index=False)

print("数据清洗完成，已保存至 cleaned_job_requirements.xlsx")

