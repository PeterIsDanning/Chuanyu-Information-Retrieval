from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://gs.swufe.edu.cn/index/xwzx.htm"

driver.get(url)
div = driver.find_element(By.CSS_SELECTOR, "div.cont")
div.click()
content = div.get_attribute('outerHTML')

soup = BeautifulSoup(content, 'html.parser')
items = soup.find_all("a", class_="list_item")
date_list = []
title_list = []
web_list = []

for item in items:
    date = item.find("div", class_="date").text
    title = item.find("h1").text
    web = "https://gs.swufe.edu.cn" + item["href"][2:]
    date_list.append(date)
    title_list.append(title)
    web_list.append(web)

df = pd.DataFrame({
    "date": date_list,
    "title": title_list,
    "web": web_list
})

df.to_csv("data/swufe_news.csv", index=False)