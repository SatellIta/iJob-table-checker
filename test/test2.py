import requests, re, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0')
options.add_argument('--accept-language=zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')

driver = webdriver.Edge(options=options)

# 先访问域名主页
# driver.get("https://career.fudan.edu.cn/")
# time.sleep(1)

# 添加您浏览器中的Cookie


driver.get("https://career.fudan.edu.cn/Zhaopin/zuijin.html?id=da9d40e5-8957-5f53-3bb8-c3f399079b3c")
WebDriverWait(driver, 3)
response = driver.execute_script("return document.documentElement.outerHTML")



with open('page.html', 'w', encoding='utf-8') as f:
    f.write(response)

response = str(response)
start_text = "<h4><span>南昌市2025年定向引进卫生专业技术人才"
end_text = "本校提示</h3>"
start_index = response.find(start_text)
end_index = response.find(end_text)
if start_index != -1 and end_index != -1:
    page = response[start_index:end_index]
            
page = BeautifulSoup(page, 'lxml')
clean_page = page.get_text(separator='\n', strip = True)
print(clean_page)