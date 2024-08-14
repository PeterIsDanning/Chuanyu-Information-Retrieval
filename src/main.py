from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

import datetime
import pandas as pd

from spider_easymoney import daily_news_spider
from script.data_processing import easymoney_df_generator
from script.docx_processing import easymoney_docx_generator

# 设置 EdgeOptions
options = EdgeOptions()
options.add_argument("--headless")  # 无头模式
# 初始化 WebDriver
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

today = datetime.datetime.now().strftime("%m-%d")
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m-%d")
companies = pd.read_csv("data/sichuan.csv")

urls = companies["website"]
names =  companies["name"]
codes = companies["code"]

name_list, code_list, title_list, web_list, info_list, abstract_list = daily_news_spider(driver=driver, urls=urls, date=yesterday, names=names, codes=codes)
df = easymoney_df_generator(name_list, code_list, title_list, web_list, info_list, abstract_list)
easymoney_docx_generator(yesterday, df)
