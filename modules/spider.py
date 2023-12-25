from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from sleep import random_sleep
from config import read_spider_config
from database_manager import DatabaseManager
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import os
import sys
from proxy import terminal as proxy_terminal
from webdriver import CustomWebDriver
from random_proxy import proxy
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
headless, images, pagesnum = read_spider_config()
sql = DatabaseManager()

def baidu_spider(keywords,use_proxy=None):
    if use_proxy == "y":
        webdriver = CustomWebDriver(
            headless=False,
            user_agent=None,  # 使用默认的 User-Agent
            proxy_server=proxy(),  # 使用默认的代理服务器
            block_images=2
        )
    else:
        webdriver = CustomWebDriver(
        headless=False,
        user_agent=None,  # 使用默认的 User-Agent
        proxy_server=None,  # 使用默认的代理服务器
        block_images=2
        )
    url = "https://www.baidu.com"
    keywords_string = keywords.split('\n')
    for keyword in keywords_string:
        try:
            webdriver.navigate(url)
            print("正在打开百度")
            random_sleep(2, 3)

            keyword = str(keyword)
            input_locator = (By.ID, 'kw')
            print("正在搜索关键字:\n" + keyword)
            webdriver.find_and_input(input_locator,keyword)
            # 搜索关键词
            click_locator = (By.ID, 'su')
            webdriver.click_element(click_locator)
            # driver.find_element().send_keys(keyword)
            # random_sleep(2, 3)
            # # print(driver.page_source)
            # btnParent = driver.find_element(By.ID, 'su')
            # btnParent.click()
            random_sleep(2, 3)

            for i in range(1, pagesnum + 1):
                print("第{}页".format(i))
                random_sleep(5, 6)

                # 数据保存
                page_source = webdriver.get_page_source()
                # print(page_source)

                baidu_html_save(i, page_source)
                click_locator = (By.CSS_SELECTOR, 'a+ .n')
                webdriver.click_element()
                # driver.find_element(By.CSS_SELECTOR, 'a+ .n').click()
        except Exception as e:
            print(f"爬虫出现错误: {e}")

        webdriver.quit()


def google_spider(keywords, use_proxy=None):
    if use_proxy == "y":
        webdriver = CustomWebDriver(
            headless=False,
            user_agent=None,  # 使用默认的 User-Agent
            proxy_server=proxy,  # 使用默认的代理服务器
            block_images=2
        )
    else:
        webdriver = CustomWebDriver(
        headless=False,
        user_agent=None,  # 使用默认的 User-Agent
        proxy_server=None,  # 使用默认的代理服务器
        block_images=2
        )
    # 1
    # https://g.luciaz.me/
    # 验证你是否来自浙江大学，三个问题的答案分别是：心灵之约、水朝夕、csxy@123

    # 2
    # https://search.ahau.cf/

    # 3
    # https://search.ecnu.cf/

    # 4
    # https://google.tigermed.net/
    keywords_string = keywords.split('\n')
    for keyword in keywords_string:
        try:
            url = "https://google.tigermed.net/"

            print("正在访问的镜像网站地址为:\n"+url)

            # driver.get(url)
            webdriver.navigate(url)

            keyword = "北京 inurl:asp?id=20"

            print("正在搜索关键字:\n"+keyword)

            random_sleep(2,3)
            input_click = (By.CSS_SELECTOR,'#APjFqb')
            webdriver.find_and_input(input_click, keyword)
            # search = driver.find_element(By.CSS_SELECTOR,'#APjFqb').send_keys(keyword)
            
            random_sleep(2,3)

            enter_click  = (By.CSS_SELECTOR,'#APjFqb')
            webdriver.enter_element(enter_click)
            random_sleep(2,3)

            for i in range(0,pagesnum):
            #模拟滑动
                print("正在下滑加载")
                script = "window.scrollTo(0,document.body.scrollHeight)"

                webdriver.execute_script(script)

                random_sleep(5,6)

                element_locator = (By.CSS_SELECTOR,'.hlcw0c')
                count = webdriver.element_count(element_locator)

                print(f'页面中有 {count} 个样式为 "hlcw0c" 的标签。')
            

            page_source = webdriver.get_page_source()
            google_html_save(page_source)

        except Exception as e:
            print(f"爬虫出现错误: {e}")
        
        webdriver.quit()

def google_html_save(page_source):
    try:
        # 数据保存
        page_source = webdriver.get_page_source()
        # print(page_source)
        # with open('google.html','w',encoding='utf-8') as f:
        #     f.write(page_source)
        
        # 数据榨取
        soup = BeautifulSoup(page_source, 'lxml')
        titles = soup.select('h3[class="LC20lb MBeuO DKV0Md"]')
        # urls = soup.select('cite[class="qLRx3b tjvcx GvPZzd cHaqb"]')
        urls = soup.select('a[jsname="UWckNb"]')
        sites = soup.select('span[class="VuuXrf"]')
        combined_elements = list(zip(titles,sites,urls))
        #UWckNb
        for index,(title,site,url) in enumerate(combined_elements):
            url = url.get('href')
            print("站点"+str(index+1))
            title_text = title.get_text()
            print("标题:"+title.get_text())
            site_text = site.get_text()
            print("站点名称:"+site.get_text())
            print("url:"+url)
            sql.insert_into_result(title_text, site_text, None, url, 1, 0, 0)

    except Exception as e:
        print(f"数据保存出现错误: {e}")

def baidu_html_save(i, page_source):
    try:
        # 数据榨取
        soup = BeautifulSoup(page_source, 'lxml')
        titles = soup.select('h3[class="c-title t t tts-title"]')
        sites = soup.select('span[class="c-color-gray"]')
        urls = soup.select('a[jsname="UWckNb"]')
        combined_elements = list(zip(titles, sites, urls))
        for index, (title, site, url) in enumerate(combined_elements):
            print("站点" + str((i - 1) * 10 + index + 1))
            title_text = title.get_text()
            print("标题:" + title_text)
            site_text = site.get_text()
            print("站点名称:" + site_text)
            link = title.find('a')['href']
            print("link:" + link)
            # 插入数据
            sql.insert_into_result(title_text, site_text, link, None, 0, 0, 0)
    except Exception as e:
        print(f"数据保存出现错误: {e}")

def process_string(string):
    # 检查字符串是否是文件名
    if os.path.isfile(string):
        # 如果是文件名，则获取文件内容并返回
        with open(string, 'r') as file:
            content = file.read()
        return content
    else:
        # 如果不是文件名，则直接返回原始字符串
        return string
    


def terminal():

    # 设置自动完成列表
    words = ['?', 'help', 'result', 'spider', 'proxy', 'quit', 'exit']
    word_completer = WordCompleter(words)
    session = PromptSession()
    
    while True:

        try:
            option = session.prompt('spider>', completer=word_completer)
            # print('You entered:', option)
            option = str(option)
        except KeyboardInterrupt:  # 捕捉 Ctrl+C
            print('KeyboardInterrupt: Exiting...')
            break

        if option == "?" or option.lower() == "help":

                print("result 输出爬虫结果")
                print("spider 爬虫")
                print("proxy 代理配置")

        elif option.lower() == "result":
            results = sql.select_urls_from_result()

            for row in results:
                print(row)

        elif option.lower() == "spider":
            # 设置自动完成列表
            words = ['?', 'help', 'baiduspider', 'googlespider', 'proxy', 'quit', 'exit']
            word_completer = WordCompleter(words)
            session = PromptSession()
            try:
                option = session.prompt('spider\spider>', completer=word_completer)
                # print('You entered:', option)
                option = str(option)
            except KeyboardInterrupt:  # 捕捉 Ctrl+C
                print('KeyboardInterrupt: Exiting...')
                break
            if option == "?" or option.lower() == "help":

                print("baiduspider")
                print("googlespider")
                print("proxy 代理配置")
            elif option.lower() == "baiduspider":
                use_proxy = input('是否使用代理(y/n)?')
                string = input('请输入要搜索的内容或者关键词文件路径')
                keywords = process_string(string)
                baidu_spider(keywords,use_proxy)

            elif option.lower() == "googlespider":
                use_proxy = input('是否使用代理(y/n)?')
                string = input('请输入要搜索的内容或者关键词文件路径')
                keywords = process_string(string)
                google_spider(keywords,use_proxy)

            elif option.lower() == "proxy":
                proxy_terminal()

            elif option.lower() == "exit" or option.lower() == "quit":
                return
            
        elif option.lower() == "proxy":
            proxy_terminal()
        elif option.lower() == "exit" or option.lower() == "quit":
            webdriver.close()
            return
        

if __name__ == "__main__":
    terminal()
    # google_spider()
