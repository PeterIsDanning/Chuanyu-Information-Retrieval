from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd


def fetch(driver: webdriver.Remote, url: str) -> Tuple[List[str], str]:
    """
    从给定URL抓取页面信息和摘要。

    该函数首先尝试从 "div.infos" 元素中获取结构化信息。如果找不到该元素，则调用 fetch_addition 函数获取额外信息。

    参数:
        driver: 一个 Selenium webdriver 实例，用于浏览器自动化。
        url: 要抓取的网页的 URL。

    返回:
        一个包含两个元素的元组：
            - item_list: 一个列表，包含从页面中提取的结构化信息（如果可用）。
            - abstract: 页面的摘要文本。
    """

    driver.get(url)

    # 尝试获取主要信息区域
    try:
        div_inter = driver.find_element(By.CSS_SELECTOR, "div.main")
        div_inter.click()  # 可能需要点击展开信息
        content_inter = div_inter.get_attribute('outerHTML')
        soup = BeautifulSoup(content_inter, 'html.parser')
        info = soup.find("div", class_="infos")  # 结构化信息区域
        if info is None:
            # 如果找不到主要信息区域，则尝试获取额外信息
            item_list, abstract = fetch_addition(driver, url)
        else:
            item_list = []
            for item in info.find_all("div", class_="item"):
                item_list.append(item.text.strip())

            # 获取页面摘要
            div_main = driver.find_element(By.CSS_SELECTOR, "head")
            content_main = div_main.get_attribute('outerHTML')
            soup_main = BeautifulSoup(content_main, 'html.parser')
            abstract = soup_main.find("meta", attrs={"name": "description"})["content"]
    except Exception as e:  # 处理异常，防止爬虫中断
        print(f"Error fetching from main area: {e}")
        item_list, abstract = fetch_addition(driver, url)  # 尝试获取额外信息
    return item_list, abstract


def fetch_addition(driver: webdriver.Remote, url: str) -> Tuple[List[str], str]:
    """
    从给定URL抓取额外信息和摘要。

    当主信息区域无法获取时，这个函数作为备用方案，从 "div.article.page-article" 元素中提取信息。

    参数:
        driver: 一个 Selenium webdriver 实例，用于浏览器自动化。
        url: 要抓取的网页的 URL。

    返回:
        一个包含两个元素的元组：
            - item_list: 一个列表，包含从页面中提取的额外信息。
            - abstract: 页面的摘要文本（第一段文本）。
    """

    driver.get(url)

    div_inter = driver.find_element(By.CSS_SELECTOR, "div.article.page-article")  # 额外信息区域
    div_inter.click()
    content_inter = div_inter.get_attribute('outerHTML')
    soup = BeautifulSoup(content_inter, 'html.parser')

    # 获取页面摘要（第一段文本）
    abstract = soup.find("p").text

    # 提取信息
    source = soup.find("a", class_="auth name")
    info = soup.find_all("span", class_="txt")

    item_list = []
    if source:  # 检查 source 是否存在
        item_list.append(source.text.strip())
    for item in info:
        item_list.append(item.text.strip())
    
    return item_list, abstract

# 每日资讯
def daily_news_spider(driver: webdriver.Remote, urls: List[str], date: str, names: List[str], codes: List[str]) -> Tuple[
    List[str], List[str], List[str], List[str], List[List[str]], List[str]
]:
    """
    从给定的URL列表中抓取指定日期的新闻，并获取相关公司的名称、代码、标题、链接、详细信息和摘要。

    参数:
        driver: 一个 Selenium webdriver 实例，用于浏览器自动化。
        urls: 要抓取新闻的网页 URL 列表。
        date: 目标日期，格式为 "MM-DD"（例如 "07-30"）。
        names: 与URL列表对应的公司名称列表。
        codes: 与URL列表对应的公司代码列表。

    返回:
        一个包含六个列表的元组：
            - name_list: 出现新闻的公司名称列表。
            - code_list: 出现新闻的公司代码列表。
            - title_list: 新闻标题列表。
            - web_list: 新闻链接列表。
            - info_list: 新闻详细信息列表（每个新闻的详细信息为一个列表）。
            - abstract_list: 新闻摘要列表。
    """

    name_list = []
    code_list = []
    title_list = []
    web_list = []
    info_list = []
    abstract_list = []

    # 遍历每个URL进行抓取
    for i in range(len(urls)):
        driver.get(urls[i])

        div = driver.find_element(By.CSS_SELECTOR, "div.qnb_list")  # 新闻列表区域
        div.click()  # 可能需要点击展开列表
        content = div.get_attribute('outerHTML')

        soup = BeautifulSoup(content, 'html.parser')
        titles = soup.find_all("a", class_="short")  # 新闻标题
        times = soup.find_all("span", class_="time")  # 新闻时间

        for time, title in zip(times, titles):
            # 筛选指定日期的新闻
            if date == time.text:
                print(title['href'])  # 打印新闻链接，方便调试
                
                # 保存相关信息
                name_list.append(names[i])
                code_list.append(codes[i])
                title_list.append(title['title'])
                web_list.append(title['href'])

                # 调用 fetch 函数获取详细信息和摘要
                item_list, abstract = fetch(driver, title["href"])
                info_list.append(item_list)
                abstract_list.append(abstract)

    return name_list, code_list, title_list, web_list, info_list, abstract_list
