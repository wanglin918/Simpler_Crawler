from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import random
import requests


#chrome_options设置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')#无头模式
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])#关闭日志
chrome_options.add_argument('--disable-gpu') # 禁用GPU加速
chrome_options.add_argument('--start-maximized')#浏览器最大化
# 关闭'Chrome目前受到自動測試軟體控制'的提示
chrome_options.add_experimental_option('useAutomationExtension', False)
prefs = {
        "download.default_directory":"D:\download",  # 设置浏览器下载地址(绝对路径)
        "profile.managed_default_content_settings.images": 2,  # 不加载图片
}
chrome_options.add_experimental_option('prefs', prefs)  # 添加prefs
driver = webdriver.Chrome(options=chrome_options)
#屏蔽标记
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})



def random_sleep(start,end):

    t = random.uniform(start,end)
    print("随机暂停{}秒".format(t))
    time.sleep(t)

def baidu_spider():
    
    url = "https://www.baidu.com"

    print("正在打开百度")
    driver.get(url)
    wait = WebDriverWait(driver,10)
    random_sleep(2,3)
    keyword = "北京"

    print("正在搜索关键字:\n"+keyword)
    
    
    #搜索关键词
    driver.find_element(By.ID,'kw').send_keys(keyword)
    random_sleep(2,3)
    #print(driver.page_source)
    btnParent = driver.find_element(By.ID,'su')
    btnParent.click()
    random_sleep(2,3)
    page = 5
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

    
    
    input('是否要关闭浏览器?')
    driver.quit()







baidu_spider()



