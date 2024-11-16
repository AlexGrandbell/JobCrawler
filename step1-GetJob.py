#Created by AlexGrandbell on 2024/11/11
#本文件用于爬取智联招聘相关职位信息
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

#读取地区编号文件
region_df = pd.read_excel("region_codes.xlsx")

#用户输入职位和地区
job_name = input("请输入职位名称：")
region_name = input("请输入地区名称：")
max_page = int(input("请输入需要爬取的最大页数："))  #让用户输入最大页数

#查找地区编号
region_code_row = region_df[region_df['地区名称'] == region_name]
if not region_code_row.empty:
    region_code = region_code_row['地区码'].values[0]
else:
    print("未找到该地区，请检查输入的地区名称是否正确。")
    exit()

#初始化浏览器
browser = webdriver.Edge()

#用于存储职位信息
job_data = []

#循环爬取多个页面
for page in range(1, max_page + 1):  #从第1页开始，直到最大页数
    url = f"https://sou.zhaopin.com/?kw={job_name}&jl={region_code}&p={page}"  #修改 URL，添加页码参数
    browser.get(url)
    time.sleep(3)  #等待页面加载

    #获取招聘职位链接
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    job_links = soup.find_all('a', class_='jobinfo__name')

    #提取每个职位的任职要求
    for link in job_links:
        job_url = link.get('href')
        browser.get(job_url)
        time.sleep(1)  #等待页面加载

        job_soup = BeautifulSoup(browser.page_source, 'html.parser')
        requirement_section = job_soup.find('div', class_='describtion__detail-content')

        if requirement_section:
            requirements = requirement_section.get_text(separator=" ").strip()
            job_data.append({
                '职位名称': link.get_text(),
                '链接': job_url,
                '任职要求': requirements
            })

#保存数据到Excel
job_df = pd.DataFrame(job_data)
job_df.to_excel("job_requirements.xlsx", index=False)

#关闭浏览器
browser.quit()

print("爬取完成，数据已保存至 job_requirements.xlsx")



