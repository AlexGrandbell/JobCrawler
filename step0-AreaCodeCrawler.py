#Created by AlexGrandbell on 2024/11/11
#本文件用于爬取智联招聘的省份代码
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

#设置浏览器驱动
browser = webdriver.Edge()

#创建一个空列表来保存地区码和地区名称
region_data = []

#循环遍历地区码从530到600
for region_code in range(530, 540):
    url = f"https://sou.zhaopin.com/?kw=数据挖掘&jl={region_code}"
    browser.get(url)
    time.sleep(3)  #等待页面加载完成

    #获取页面源码
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    #查找地区信息
    region_name_tag = soup.find('a', class_='content-s__item__text content-s__item__text--active')

    if region_name_tag:
        region_name = region_name_tag.get_text()
        region_data.append({'地区码': region_code, '地区名称': region_name})
    else:
        #如果没有找到地区名称，跳过
        print(f"地区码 {region_code} 未找到地区名称")
        continue

#将结果保存到 DataFrame
df = pd.DataFrame(region_data)

#将结果写入 Excel 文件
df.to_excel("region_codes.xlsx", index=False)

#关闭浏览器
browser.quit()

print("爬取完成，数据已保存至 region_codes.xlsx")