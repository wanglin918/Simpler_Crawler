from bs4 import BeautifulSoup
from sleep import random_sleep
from selenium import webdriver
from config import read_proxy_config as read_config
from selenium.webdriver.common.by import By
from database_manager import DatabaseManager
import requests

headless_mode, images_mode, proxies_num, max_retries = read_config()

def proxy_spider():

    
    #chrome_options设置
    chrome_options = webdriver.ChromeOptions()

    if(headless_mode == False):
        chrome_options.add_argument('--headless')#无头模式

    #chrome_options.add_argument("--proxy-server=http://127.0.0.1:7890")

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

    sql = DatabaseManager()
    sql.create_proxypool_table()
    num = sql.select_proxypool_num()


    if num >=proxies_num:

        print("代理库记录数已超过{}".format(proxies_num))
        print("下面将直接进行测试")
        proxy_test()

    count = 1

    source_option = 3
    
    option3_istest = False


    while num <= proxies_num :
        
        if source_option == 1:

            url = "https://www.kuaidaili.com/free/"
    
        elif source_option == 2:

            url = "https://www.89ip.cn/"
            
        elif source_option == 3:

            if option3_istest == False:
                Get_proxylist()
            else:
                url = "https://www.89ip.cn/"

        print("代理库记录数未超过{}".format(proxies_num))

        print("正在从{}中获取代理".format(url))

        driver.get(url)

        random_sleep(1,2)

        page_source = driver.page_source

        if url == "https://www.kuaidaili.com/free/":

            kuaidaili_proxy_save(page_source)
            for y in range(100):
                js='window.scrollBy(0,6.6)'
                driver.execute_script(js)
                random_sleep(0.2,0.5)
            driver.find_element(By.CSS_SELECTOR,'input').send_keys(str(count+1))
            random_sleep(0.5,1)
            driver.find_element(By.CSS_SELECTOR,'input').click()
        elif url == "https://www.89ip.cn/":
            #1039.912353515625
            www89ipcn_proxy_save(page_source)
            for y in range(100):
                js='window.scrollBy(0,11)'
                driver.execute_script(js)
                random_sleep(0.1,0.2)

            driver.find_element(By.LINK_TEXT,'下一页').click()

        proxy_test()

        num = sql.select_proxypool_num()
        
    driver.quit()

def kuaidaili_proxy_save(page_source):

    with open('proxy.html','w',encoding='utf-8') as f:
        f.write(page_source)

    #数据榨取
    soup = BeautifulSoup(open('proxy.html',encoding='utf-8'),'lxml')
    
    IP = soup.select('td[data-title="IP"]')
    PORT = soup.select('td[data-title="PORT"]')
    LEVEL = soup.select('td[data-title="匿名度"]')
    TYPE = soup.select('td[data-title="类型"]')
    SPEED = soup.select('td[data-title="响应速度"]')
    LASTTIME = soup.select('td[data-title="最后验证时间"]')
    combined_elements = list(zip(IP,PORT,LEVEL,TYPE,SPEED,LASTTIME))

    for index,(IP,PORT,LEVEL,TYPE,SPEED,LASTTIME) in enumerate(combined_elements):

        ip = IP.get_text()
        port = PORT.get_text()
        level = LEVEL.get_text()
        type = TYPE.get_text()
        speed = SPEED.get_text()
        lasttime = LASTTIME.get_text()
        #print(float(speed.strip("秒")))
        # print(IP.get_text())
        # print(PORT.get_text())
        # print(LEVEL.get_text())
        # print(TYPE.get_text())
        # print(SPEED.get_text())
        # print(LASTTIME.get_text())
        

        
        value = float(speed.strip("秒"))

        if value <= 1:

            sql = DatabaseManager()

            sql.create_proxypool_table()

            sql.insert_into_proxypool(ip, port, level, type, speed,lasttime,0)

def www89ipcn_proxy_save(page_source):

    with open('proxy.html','w',encoding='utf-8') as f:
            f.write(page_source)

    #数据榨取
    soup = BeautifulSoup(open('proxy.html',encoding='utf-8'),'html.parser')

    # 查找所有的<tr>标签
    rows = soup.find_all('tr')

    # 循环遍历每个<tr>标签，并提取其中的数据
    for row in rows[1:]:  # 从第二个<tr>开始遍历
        # 查找<td>标签
        data = row.find_all('td')
        
        # 分别提取<td>中的数据
        ip = data[0].get_text(strip=True)
        port = data[1].get_text(strip=True)
        #location = data[2].get_text(strip=True)
        #provider = data[3].get_text(strip=True)
        last_update = data[4].get_text(strip=True)

        sql = DatabaseManager()
        sql.insert_into_proxypool(ip,port,"","","",last_update,0)
        # # 打印每个变量的值
        # print(f"IP: {ip}")
        # print(f"Port: {port}")
        # #print(f"Location: {location}")
        # #print(f"Provider: {provider}")
        # print(f"Last Update: {last_update}")

def Get_proxylist():

    import json
    countryonly="CN"

    print("[*] Getting ip from proxylist.fatezero . . .")
    fpl_url = "http://proxylist.fatezero.org/proxy.list"
    proxy_list = requests.get(fpl_url)
    if proxy_list.status_code == 200:
        lines = proxy_list.text.split('\n')
        for i,line in enumerate(lines):
            
            # print(f"Index {i} : {line}")
            try:
                content = json.loads(line)
                # print(content["host"])
            except:
                continue
            if str(content["country"]) == countryonly:
                sql = DatabaseManager()
                sql.insert_into_proxypool(str(content["host"]),str(content["port"]),str(content["anonymity"]),str(content["type"]),str(content["response_time"]),"",0)
                ip_port = str(content["host"]) + ":" + str(content["port"])
                print(ip_port)
                
            
        print("processed {} in free proxy list".format(str(i)))
    proxy_test()

def proxy_test():

    sql = DatabaseManager()

    results = sql.select_ip_port_from_proxypool()

    for row in results:

        ip, port = row

        proxy_url = f"http://{ip}:{port}"

        #print(proxy_url)  # 假设每个元组只包含一个IP地址字段

        proxies = {

            "http":proxy_url

        }


        # 标记是否成功通过测试
        success = False

        for _ in range(max_retries):
            try:
                from user_agent import GetUserAgent
                user_agent = GetUserAgent()
                headers = {"User-Agent": user_agent}
                url = "http://httpbin.org/get"
                response = requests.get(url=url, headers=headers, proxies=proxies,timeout=(2,5))

                random_sleep(0.5, 1)

                # 检查响应状态码
                if response.status_code == 200:
                    print("Request successful")
                    sql.update_proxypool(ip)
                    success = True
                    break  # 成功后跳出循环

                else:
                    print(f"Request failed with status code {response.status_code}")

            except Exception as e:
                print(f"An error occurred: {str(e)}")

        # 如果没有成功通过测试，则删除代理 IP
        if not success:
            sql.delete_ip_from_proxypool(ip)

        



if __name__ == "__main__":

    #headless, images, proxies_num = read_config()

    proxy_spider()
    #proxy_test()

