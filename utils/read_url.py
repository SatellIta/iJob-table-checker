import re, time
from .conference_info import Conference
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from UI.some_dialog import FailWebMessage

def analyze_info():
    '''
    分析招聘网信息的主函数
    '''
    main_page = open_url()
    if not main_page:
        return None    
    
    titles, urls = read_url(main_page)
    if not urls:
        return None
    
    conferences = []
    conferences = read_page(titles, urls)
    
    return conferences


def open_url():
    '''
    尝试打开复旦大学招聘信息网
    失败弹出错误报告
    成功返回含所有段包落的列表，调用read_url()进一步处理
    '''
    try:
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        # 反检测配置
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0')
        options.add_argument('--accept-language=zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        driver = webdriver.Edge(options=options)

        driver.get("https://career.fudan.edu.cn/Zhaopin/talk.html")

        if driver.page_source:
            response = driver.page_source
            driver.quit()
            return response
        else:
            raise ValueError("页面内容为空")
        
    except ValueError as e:
        oops = FailWebMessage(None, str(e))
        oops.exec()
        return None
    
    except ConnectionError as e:
        oops = FailWebMessage(None, str(e))
        oops.exec()
        return None
    
    except TimeoutError as e:
        oops = FailWebMessage(None, str(e))
        oops.exec()
        return None

    except Exception as e:
        oops = FailWebMessage(None, str(e))
        oops.exec()
        return None
    
def read_url(main_page):
    '''
    读取主页面，返回包含所有宣讲会链接的列表
    根据系统时间查找第二天的宣讲会
    没有找到则返回none
    '''
    # 以'mm-dd'形式保存日期信息
    aim_date = time.localtime()
    day = int(time.strftime("%d", aim_date)) + 1
    day = str(day)
    month = time.strftime("%m", aim_date)
    aim_date = month + '-' + day

    # 匹配结果返回一个元组, 第一个元素为标题, 第二个元素为url
    date_pattern = re.compile(f'<a href="(.+?)".+?><div class="ol_left"><p style.+?>{aim_date}.+?<p title="(.+?)" class="ol_title">')
    results = re.findall(pattern=date_pattern, string=main_page)
    if results:
        titles = []
        urls = []
        for res in results:
            titles.append(res[1])
            urls.append("https://career.fudan.edu.cn" + res[0])

        return titles, urls
    else:
        return None, None

def read_page(titles, urls):
    options = Options()
    # 无头模式
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    # 反检测配置
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0')
    options.add_argument('--accept-language=zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')

    driver = webdriver.Edge(options=options)
    
    conferences = []
    for index in range(0, len(urls)):
        try:
            driver.get(urls[index])
            WebDriverWait(driver, 5)
            page = str(driver.execute_script("return document.documentElement.outerHTML"))
            
            if not page:
                raise ConnectionError("在查找宣讲会时出错")
            
            # 开始匹配提取信息, 看到一大串html标签, 觉得还是得使用beautifulsoup来提取文本
            start_text = "<h4><span>" + titles[index]
            end_text = "本校提示</h3>"
            start_index = page.find(start_text)
            end_index = page.find(end_text)
            if start_index != -1 and end_index != -1:
                page = page[start_index:end_index]
            
            page = BeautifulSoup(page, 'lxml')
            clean_page = page.get_text(separator='\n', strip = True)
            conferences.append(create_conf(index, clean_page, titles[index]))
            
        except ConnectionError as e:
            conferences.append(create_conf(index, e))
    
    driver.quit()
    return conferences

def create_conf(index, text, title):
    if text == "在查找宣讲会时出错":
        return Conference(
        index=index + 1,
        title=text,
        place=None,
        date=None,
        time=None,
        detail=None
    )

    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    date_match = date_pattern.search(text)
    if date_match:
        date = date_match.group(0).strip()

    time_pattern = re.compile(r'\d{2}:\d{2}-\d{2}:\d{2}')
    time_match = time_pattern.search(text)
    if time_match:
        time = time_match.group(0).strip()

    place_pattern = re.compile(r'详细地址[:：]\s*(.*)')
    place_match = place_pattern.search(text)
    if place_match:
        place = place_match.group(1).strip()

    # 匹配到的文段是"宣讲会详情: .*"，因此截断，去掉"宣讲会详情："只保留主要内容
    text = str(text)
    start_idx = text.find("宣讲会详情")
    if start_idx != -1:
        text = text[start_idx + len("宣讲会详情"): ]
        detail = text.replace('\n', '')
        #print(detail)
    
    return Conference(
        index=index + 1,
        title=title,
        place=place,
        date=date,
        time=time,
        detail=detail
    )