from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re, time

options = Options()
# 无头模式
options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')
# 反检测配置
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0')
options.add_argument('--accept-language=zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')

driver = webdriver.Edge(options=options)

driver.get("https://career.fudan.edu.cn/Zhaopin/zuijin.html?id=d6f457ce-614e-d393-c775-2a441a363bc4")
WebDriverWait(driver, 5)
page = str(driver.execute_script("return document.documentElement.outerHTML"))

with open('page.html', 'w', encoding='utf-8') as f:
    f.write(page)

