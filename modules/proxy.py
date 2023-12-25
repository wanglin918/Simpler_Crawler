from bs4 import BeautifulSoup
from sleep import random_sleep
from config import read_proxy_config as read_config
from selenium.webdriver.common.by import By
from database_manager import DatabaseManager
import requests
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from webdriver import CustomWebDriver
from random_proxy import proxy
headless_mode, images_mode, proxies_num, max_retries, expiration_time = read_config()
sql = DatabaseManager()

def proxy_spider(option_get,use_proxy=None):
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
    num = sql.select_proxypool_num()

    if num >= proxies_num:
        print("有效代理数已超过设定数:{}".format(proxies_num))
        return

    else:

        print("有效代理数未超过设定数:{}".format(proxies_num))

        print("正在从 {} 中获取代理".format(option_get))

        count = 1
        
        proxylist_istest = False


        while num <= proxies_num :

            if option_get == "zdaye":

                url = "https://www.zdaye.com/free/"
            
            elif option_get == "kuaidaili":

                url = "https://www.kuaidaili.com/free/"
        
            elif option_get == "89ip":

                url = "https://www.89ip.cn/"
                
            elif option_get == "proxylist":

                if proxylist_istest == False:
                    Get_proxylist()
                    proxylist_istest = True

                else:
                    print("proxylist代理已提取完毕")
                    return

            webdriver.navigate(url)
            page_source = webdriver.get_page_source()
            random_sleep(1,2)

            if url == "https://www.zdaye.com/free/":

                zhandaye_proxy_save(page_source)

            elif url == "https://www.kuaidaili.com/free/":
                kuaidaili_proxy_save(page_source)
                
                for y in range(100):
                    webdriver.scroll_down(6.6)
                    random_sleep(0.2,0.5)
                input_locator = (By.CSS_SELECTOR,'input')
                webdriver.find_and_input(input_locator, str(count+1))
                #driver.find_element(By.CSS_SELECTOR,'input').send_keys(str(count+1))
                random_sleep(0.5,1)
                webdriver.click_element(input_locator)
                #driver.find_element(By.CSS_SELECTOR,'input').click()
            
            elif url == "https://www.89ip.cn/":
                #1039.912353515625
                www89ipcn_proxy_save(page_source)
                for y in range(100):
                    webdriver.scroll_down(11)
                    random_sleep(0.1,0.2)
                click_locator = (By.LINK_TEXT,'下一页')
                webdriver.click_element(click_locator)
                #driver.find_element(By.LINK_TEXT,'下一页').click()

            proxy_test()

            num = sql.select_proxypool_num()
            
        webdriver.close()

def zhandaye_proxy_save(page_source):
    #数据榨取
    soup = BeautifulSoup(page_source,'html.parser')

    # 查找所有的<tr>标签
    rows = soup.find_all('tr')

    # 循环遍历每个<tr>标签，并提取其中的数据
    for row in rows[1:]:  # 从第二个<tr>开始遍历
        # 查找<td>标签
        data = row.find_all('td')
        
        # 分别提取<td>中的数据
        ip = data[0].get_text(strip=True)
        port = data[1].get_text(strip=True)
        level = data[2].get_text(strip=True)
        #provider = data[3].get_text(strip=True)
        # last_update = data[4].get_text(strip=True)
        div_iyes = data[5].find("div", class_="iyes")
        if div_iyes:
            type = "https"
        else:
            type = "http"
        speed = data[6].get_text(strip=True)
        sql = DatabaseManager()
        sql.insert_into_proxypool(ip,port,level,type,speed,"",0)

def kuaidaili_proxy_save(page_source):

    #数据榨取
    soup = BeautifulSoup(page_source,'lxml')
    
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

    # with open('proxy.html','w',encoding='utf-8') as f:
    #         f.write(page_source)

    #数据榨取
    soup = BeautifulSoup(page_source,'html.parser')

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

                sql.insert_into_proxypool(str(content["host"]),str(content["port"]),str(content["anonymity"]),str(content["type"]),str(content["response_time"]),"",0)
                ip_port = str(content["host"]) + ":" + str(content["port"])
                print(ip_port)
                
            
        print("processed {} in free proxy list".format(str(i)))
    proxy_test()

def proxy_test():

    results = sql.select_ip_port_from_proxypool()

    for row in results:

        ip, port = row

        proxy_http = f"http://{ip}:{port}"
        proxy_https  = f"https://{ip}:{port}"

        #print(proxy_url)  # 假设每个元组只包含一个IP地址字段

        proxies = {

            "http":proxy_http,
            "https":proxy_https

        }


        # 标记是否成功通过测试
        success = False

        for _ in range(max_retries):
            try:
                from user_agent import GetUserAgent
                user_agent = GetUserAgent()
                headers = {"User-Agent": user_agent}
                url = "http://httpbin.org/get"
                # url = "https://www.baidu.com"
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

def proxy_update(expiration_time):

    from datetime import datetime
        # 获取当前时间
    now = datetime.now()
    results = sql.select_ip_lasttime_from_proxypool()

    for row in results:

        ip, lasttime = row
        date_string = lasttime[0:10]
        #print(date_string)
        #print(date_string[4])

        if date_string[4] == "/":
            date_object = datetime.strptime(date_string, "%Y/%m/%d")

        elif date_string[4] == "-":
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
        
        #elif lasttime == None:
            
        time_difference = now - date_object
        # 获取时间差的天数
        days_difference = time_difference.days
        print(date_string,days_difference)

        if days_difference >= expiration_time:
            sql.delete_ip_from_proxypool(ip)

def proxies_delete():
    try:
        sql.delete_all_from_proxypool()        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def terminal():
    # 设置自动完成列表
    words = ['?', 'help', 'checknum', 'lsproxies', 'deleteall', 'getproxies', 'test', 'deleteproxies', 'quit','exit']
    word_completer = WordCompleter(words)
    session = PromptSession()

    while True:

        try:
            option = session.prompt('proxypool>', completer=word_completer)
            # print('You entered:', option)
            option = str(option)
        except KeyboardInterrupt:  # 捕捉 Ctrl+C
            print('KeyboardInterrupt: Exiting...')
            break
        if option == "?" or option.lower() == "help":

                print("checknum 查询代理池可用代理数量")
                print("lsproxies 遍历代理池可用代理")
                print("getproxies 获取代理")
                print("test 代理测试")

        elif option.lower() == "checknum":
            sql.select_proxypool_num()

        elif option.lower() == "lsproxies":
            results = sql.select_ip_port_from_proxypool()
            for row in results:
                ip = row[0]  # 假设IP在结果元组中的第一个位置
                port = row[1]  # 假设端口在结果元组中的第二个位置

                # 组合IP和端口成为一个字符串
                combined = f"{ip}:{port}"

                # 在这里你可以使用 combined 这个字符串执行你需要的操作
                print(combined)  # 示例：打印组合后的字符串

        elif option.lower() == "getproxies":

            while True:

                words_get = ['?', 'help', 'zdaye','89ip', 'kuaidaili', 'proxylist', 'quit', 'exit', 'back']
                word_completer_get = WordCompleter(words_get)
                session = PromptSession()
                try:
                    option_get = session.prompt('proxypool\getproxies>', completer=word_completer_get)
                    # print('You entered:', option)
                    option_get = str(option_get)
                except KeyboardInterrupt:  # 捕捉 Ctrl+C
                    print('KeyboardInterrupt: Exiting...')
                    break
                if option_get == "?" or option_get.lower() == "help":
                    print("可选来源:")
                    print("\tzdaye(推荐)")
                    print("\t89ip")
                    print("\tkuaidaili ")
                    print("\tproxylist ")
                elif option_get.lower() == "zdaye":
                    proxy_spider(option_get)
                elif option_get.lower() == "kuaidaili":
                    proxy_spider(option_get)

                elif option_get.lower() == "89ip":
                    proxy_spider(option_get)

                elif option_get.lower() == "proxylist":
                    proxy_spider(option_get)
                elif option_get.lower() == "exit" or option_get.lower() == "quit":
                    return
                elif option_get.lower() == 'back':
                    break
                

        elif option.lower() == "test":            
            proxy_test()
        elif option.lower() == "updateproxies":
            proxy_update(expiration_time)
        elif option.lower() == "deleteall":
            proxies_delete()
        elif option.lower() == "exit" or option.lower() == "quit":
            return
        elif option.lower() == 'back':
                    break

if __name__ == "__main__":

    #headless, images, proxies_num = read_config()
    #proxy_test()
    terminal()
    #proxy_delete(expiration_time)

    
