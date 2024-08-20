from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

import datetime
import pandas as pd

from src.spider_eastmoney import daily_news_spider
from src.spider_dongmi import daily_dongmi
from utils.data_processing import eastmoney_df_generator
from utils.docx_processing import eastmoney_docx_generator, dongmi_docx_generator


# 设置 EdgeOptions
options = EdgeOptions()
options.add_argument("--headless")  # 无头模式
# 初始化 WebDriver
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

# 初始化日期和公司信息
today = datetime.datetime.now().strftime("%m-%d")
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m-%d")
companies = pd.read_csv("data/sichuan.csv")

urls = companies["website"]
names =  companies["name"]
codes = companies["code"]

# 采集新闻并生成docx文件
name_list, code_list, title_list, web_list, info_list, abstract_list = daily_news_spider(driver=driver, urls=urls, date=yesterday, names=names, codes=codes)
df = eastmoney_df_generator(name_list, code_list, title_list, web_list, info_list, abstract_list)
eastmoney_docx_generator(today, df)

# 采集董秘问答并生成docx文件
n_list, q_list, a_list = daily_dongmi(driver, companies, yesterday)
file_path = "data/dongmi.csv"
new_data = {
    "name": n_list,
    "question": q_list,
    "answer": a_list
}
dm = pd.DataFrame(new_data)
dongmi_docx_generator(today, dm)