import requests
from sleep import random_sleep
from user_agent import GetUserAgent
from database_manager import DatabaseManager
from random_proxy import proxy as random_proxy


def ip_select():

    sql = DatabaseManager()

    link_list = sql.select_links_from_result()

    return link_list

def ip_delete(ip):

    sql = DatabaseManager()

    sql.delete_ip_from_proxypool(ip)


def test():

    max_retries = 2

    # 要检查的字符串列表
    specific_strings = ["gateway.zscloud", "origurl"]

    link_list = ip_select()
    # 打印所有值
    for row in link_list:

        link = row

        #print(link)
 
        for retry in range(max_retries):
                
            try:

                proxy = random_proxy()

                random_UA = GetUserAgent()

                headers = {

                    'User-Agent': random_UA

                }
                proxies = {
                    'http': proxy,
                    'https': proxy
                }
                response = requests.get(url=link,headers=headers,proxies=proxies,timeout=(4,10))
                if response.status_code == 200:
                    # 如果成功，返回响应对象
                    
                    real_url = response.url

                    if any(string in real_url for string in specific_strings):
                        from urllib.parse import urlparse, parse_qs

                        # 解析 URL
                        parsed_url = urlparse(real_url)

                        # 获取 URL 参数
                        url_params = parse_qs(parsed_url.query)

                        # 提取 origurl 参数
                        origurl = url_params.get('origurl', [''])[0]

                        # 解码 origurl 值
                        decoded_origurl = origurl.replace("%3A", ":").replace("%2F", "/")

                        print(decoded_origurl)

                        real_url = exception_handling(decoded_origurl)
       
                    print(real_url)

                    update_url(real_url,link)
                else:
                    print("Retrying...")
            except requests.exceptions.RequestException as e:
                print("Request failed (retry {}/{}): {}".format(retry + 1, max_retries, str(e)))
                if retry < max_retries - 1:
                    print("Retrying...")
                    random_sleep(1,2)  # 休眠一段时间后重试
                else:
                    real_url = exception_handling(link)
                    update_url(real_url,link)
                    #print("Max retries reached. Request failed.")
    else:
        print("url 已查询完毕或 url 已存在")

def update_url(real_url,link):

    sql = DatabaseManager()

    sql.update_urls_in_result(real_url,link)


def exception_handling(url):

    from selenium import webdriver

    #chrome_options设置
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])  # 关闭日志
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    prefs = {
        "download.default_directory": "D:\download",  # 设置浏览器下载地址(绝对路径)
        "profile.managed_default_content_settings.images": 2,  # 不加载图片
    }
    chrome_options.add_experimental_option('prefs', prefs)  # 添加prefs

    driver = webdriver.Chrome(options=chrome_options)

    #屏蔽标记
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    driver.get(url)

    real_url = driver.current_url

    driver.close()

    return real_url

if __name__ == "__main__":

    test()