from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import urllib.parse
import datetime

def daily_dongmi(driver: webdriver.Remote, companies: dict, date: str) -> Tuple[List[str], List[str], List[str]]:
    """
    从东方财富互动平台抓取指定公司在特定日期的互动问答数据。

    参数:
        driver: 一个 Selenium webdriver 实例，用于浏览器自动化。
        companies: 包含公司信息的字典，其中 "name" 是公司名称列表的键。
        date: 目标日期，格式为 "MM-DD"（例如 "07-30"）。

    返回:
        一个包含三个列表的元组：
            - n_list: 在指定日期有相关问答的公司名称列表。
            - q_list: 在指定日期提出的问题列表。
            - a_list: 在指定日期提供的回答列表。

    异常:
        ValueError: 如果输入的 `date` 格式不正确 (不是 "MM-DD")。
    """

    # 验证日期格式
    try:
        datetime.datetime.strptime(date, "%m-%d")
    except ValueError:
        raise ValueError("日期格式不正确，应为 MM-DD")

    n_list, q_list, a_list = [], [], []

    for company in companies["name"]:
        base_url = "https://so.eastmoney.com/qa/s?keyword="
        keyword = company
        sort = "time"
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"{base_url}{encoded_keyword}&sort={sort}"
        driver.get(url)
        # 提取并解析内容
        try:
            div = driver.find_element(By.CSS_SELECTOR, "div.qa_list")
        except:
            print(url)
        content = div.get_attribute('outerHTML')
        soup = BeautifulSoup(content, 'html.parser')

        # 检查内容是否为空
        if not soup.text.strip():
            continue  # 如果没有问答，跳过这家公司

        # 查找问答元素
        answer_times = soup.find_all("div", class_="qa_answer_date")
        questions = soup.find_all("div", class_="qa_question_text")
        answers = soup.find_all("div", class_="qa_answer_text")

        # 按日期筛选问答
        for i in range(len(answer_times)):
            time = datetime.datetime.strptime(answer_times[i].text, "%Y-%m-%d %H:%M:%S").strftime("%m-%d")
            if time == date:
                n_list.append(company)
                q_list.append(questions[i].text)
                a_list.append(answers[i].text)

    return n_list, q_list, a_list