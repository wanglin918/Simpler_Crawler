from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import requests
from config import read_config
import os

def chrome_option(headless_mode,images_mode):
    #chrome_options设置
    chrome_options = webdriver.ChromeOptions()

    if(headless_mode == False):
        chrome_options.add_argument('--headless')#无头模式

    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])#关闭日志

    chrome_options.add_argument('--disable-gpu') # 禁用GPU加速

    chrome_options.add_argument('--start-maximized')#浏览器最大化

    # 关闭'Chrome目前受到自動測試軟體控制'的提示
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {
            "download.default_directory":"D:\download",  # 设置浏览器下载地址(绝对路径)
            "profile.managed_default_content_settings.images": images_mode,  # 不加载图片
    }
    chrome_options.add_experimental_option('prefs', prefs)  # 添加prefs


    driver = webdriver.Chrome(options=chrome_options)

    #屏蔽标记
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    return driver


def random_sleep(start,end):

    t = random.uniform(start,end)
    print("随机暂停{}秒".format(t))
    time.sleep(t)

def baidu_spider(headless_mode,images_mode,pagenum,keywords):

    #chrome_options设置
    chrome_options = webdriver.ChromeOptions()

    if(headless_mode == False):
        chrome_options.add_argument('--headless')#无头模式

    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])#关闭日志

    chrome_options.add_argument('--disable-gpu') # 禁用GPU加速

    chrome_options.add_argument('--start-maximized')#浏览器最大化

    # 关闭'Chrome目前受到自動測試軟體控制'的提示
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {
            "download.default_directory":"D:\download",  # 设置浏览器下载地址(绝对路径)
            "profile.managed_default_content_settings.images": images_mode,  # 不加载图片
    }
    chrome_options.add_experimental_option('prefs', prefs)  # 添加prefs


    driver = webdriver.Chrome(options=chrome_options)

    #屏蔽标记
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    url = "https://www.baidu.com"
    
    driver.get(url)

    print("正在打开百度")
    
    
    random_sleep(2,3)
    keyword = str(keywords)

    print("正在搜索关键字:\n"+keyword)
    
    
    #搜索关键词
    driver.find_element(By.ID,'kw').send_keys(keyword)
    random_sleep(2,3)
    #print(driver.page_source)
    btnParent = driver.find_element(By.ID,'su')
    btnParent.click()
    random_sleep(2,3)
    page = pagenum
    for i in range(1,page+1):
        print("第{}页".format(i))
        random_sleep(5,6)
        #数据保存
        page_source = driver.page_source
        # print(page_source)
        with open('baidu.html','w',encoding='utf-8') as f:
            f.write(page_source)


        #数据榨取
        soup = BeautifulSoup(open('baidu.html',encoding='utf-8'),'lxml')
        titles = soup.select('h3[class="c-title t t tts-title"]')
        sites = soup.select('span[class="c-color-gray"]')
        combined_elements = list(zip(titles,sites))
        for index,(title,site) in enumerate(combined_elements):
            print("站点"+str((i-1)*10+index+1))
            print("标题:"+title.get_text())
            print("站点名称:"+site.get_text())
            link = title.find('a')['href']
            #url = requests.get(link).url
            print("url:"+url)
        driver.find_element(By.CSS_SELECTOR,'a+ .n').click()

    """# 找到要点击的元素
    element = driver.find_element(By.LINK_TEXT, '视频')

    # 创建 ActionChains 对象
    actions = ActionChains(driver)

    # 在元素上执行点击操作
    actions.click(element)

    # 执行操作
    actions.perform()"""
    
    driver.quit()



if __name__ == "__main__":
    # 调用读取配置的函数
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建相对路径
    config_file = os.path.join(current_dir, 'config.ini')
    headless, images, pages, keywords = read_config(config_file)

    
    baidu_spider(headless,images,pages,keywords)



