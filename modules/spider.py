from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from sleep import random_sleep
from config import read_spider_config
from database_manager import DatabaseManager

import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
headless, images, pagesnum, keywords = read_spider_config()

def baidu_spider():

    #chrome_options设置
    chrome_options = webdriver.ChromeOptions()

    if(headless == False):
        chrome_options.add_argument('--headless')  # 无头模式

    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])  # 关闭日志
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--start-maximized')  # 浏览器最大化

    # 关闭'Chrome目前受到自動測試軟體控制'的提示
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {
        "download.default_directory": "D:\download",  # 设置浏览器下载地址(绝对路径)
        "profile.managed_default_content_settings.images": images,  # 不加载图片
    }
    chrome_options.add_experimental_option('prefs', prefs)  # 添加prefs

    driver = webdriver.Chrome(options=chrome_options)

    #屏蔽标记
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    url = "https://www.baidu.com"

    try:
        driver.get(url)
        print("正在打开百度")
        random_sleep(2, 3)

        keyword = str(keywords)

        print("正在搜索关键字:\n" + keyword)

        # 搜索关键词
        driver.find_element(By.ID, 'kw').send_keys(keyword)
        random_sleep(2, 3)
        # print(driver.page_source)
        btnParent = driver.find_element(By.ID, 'su')
        btnParent.click()
        random_sleep(2, 3)

        sql = DatabaseManager()
        sql.create_spider_table()

        for i in range(1, pagesnum + 1):
            print("第{}页".format(i))
            random_sleep(5, 6)

            # 数据保存
            page_source = driver.page_source
            # print(page_source)

            data_save(i, page_source, sql)

            driver.find_element(By.CSS_SELECTOR, 'a+ .n').click()
    except Exception as e:
        print(f"爬虫出现错误: {e}")

    driver.quit()

def data_save(i, page_source, sql):
    try:
        # 数据榨取
        soup = BeautifulSoup(page_source, 'lxml')
        titles = soup.select('h3[class="c-title t t tts-title"]')
        sites = soup.select('span[class="c-color-gray"]')
        combined_elements = list(zip(titles, sites))
        for index, (title, site) in enumerate(combined_elements):
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

if __name__ == "__main__":
    baidu_spider()
