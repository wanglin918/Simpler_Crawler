from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from config import read_webdriver_config

import time
import os

# 获取上级目录的路径
parent_directory = os.getcwd()
chromedriver_path = os.path.join(parent_directory, "chromedriver.exe")
temp_folder_path = os.path.join(parent_directory, "temp")
print("chromedriver地址:"+chromedriver_path)
browser = read_webdriver_config()
class CustomWebDriver:
    def __init__(self, chromedriver_path = chromedriver_path,headless=True, user_agent=None, proxy_server=None, download_directory=temp_folder_path, block_images=2):
        self.options = self._create_options()
        self.service = Service(chromedriver_path)
        self.headless = headless
        self.user_agent = user_agent
        self.proxy_server = proxy_server
        self.download_directory = download_directory
        self.block_images = block_images
        self.webdriver = self._create_driver()

    def _create_options(self):
        if browser == "chrome":
            return webdriver.ChromeOptions()
        elif browser == "edge":
            return webdriver.EdgeOptions()

    def _create_driver(self):
        if self.headless:
            self.options.add_argument('--headless')  # 无头模式

        if self.user_agent:
            self.options.add_argument(f'--user-agent={self.user_agent}')  # 设置 User-Agent

        if self.proxy_server:
            self.options.add_argument(f'--proxy-server={self.proxy_server}')  # 设置代理服务器

        self.options.add_argument('--disable-gpu')  # 禁用 GPU 加速
        self.options.add_argument('--start-maximized')  # 最大化窗口
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-dev-shm-usage')  # 禁用 /dev/shm 的使用
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-breakpad')
        self.options.add_argument('--disable-client-side-phishing-detection')
        self.options.add_argument('--disable-cloud-import')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--disable-session-crashed-bubble')
        self.options.add_argument('--disable-ipv6')
        self.options.add_argument('--safebrowsing-disable-auto-update')
        self.options.add_argument('--disable-sync')
        self.options.add_argument('--disable-background-timer-throttling')
        self.options.add_argument('--disable-backgrounding-occluded-windows')
        self.options.add_argument('--disable-renderer-backgrounding')
        self.options.add_argument('--disable-features=TranslateUI,BlinkGenPropertyTrees,Worklet')  # 禁用一些功能
        self.options.add_argument('--disable-hang-monitor')
        self.options.add_argument('--disable-prompt-on-repost')
        self.options.add_argument('--disable-sync-preferences')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])  # 关闭日志
        # self.options.add_experimental_option('useAutomationExtension', False)

        if self.download_directory:
            prefs = {
                "download.default_directory": self.download_directory,  # 设置浏览器下载地址(绝对路径)
                "profile.managed_default_content_settings.images": 2,  # 不加载图片
            }
            self.options.add_experimental_option('prefs', prefs)  # 添加 prefs

        if browser == "chrome":
            self.driver = webdriver.Chrome(options=self.options,service=self.service)
        elif browser == "edge":
            self.driver = webdriver.Edge(options=self.options,service=self.service)
        

        
    def navigate(self, url):
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        self.driver.get(url)
        


    def get_page_source(self):
        return self.driver.page_source

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()

    def execute_script(self, script):
        try:
            self.driver.execute_script(script)
        except WebDriverException as e:
            print(f"Error executing script: {e}")


    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        
    def element_count(self, locator):
        try:
            elements = self.driver.find_elements(*locator)
            count = len(elements)
            return count
        except NoSuchElementException:
            return False

    def find_and_input(self, locator, text):
        """
        在页面中查找特定元素，并输入文本。
        
        Parameters:
            - locator: 元素定位器，例如 (By.ID, 'element_id')
            - text: 要输入的文本
        """
        element = self.driver.find_element(*locator)
        element.send_keys(text)
    
    def click_element(self, locator):
        """
        在页面中查找特定元素，并执行点击操作。
        
        Parameters:
            - locator: 元素定位器，例如 (By.ID, 'element_id')
        """
        element = self.driver.find_element(*locator)
        element.click()

    def enter_element(self, locator):
        """
        Parameters:
            - locator: 元素定位器，例如 (By.ID, 'element_id')
        """
        element = self.driver.find_element(*locator)
        element.send_keys(Keys.ENTER)

    def scroll_page(self, pixels, duration=0.5):
        """
        模拟垂直滚动指定像素数。
        
        Parameters:
            - pixels: 滚动的像素数，负值表示向上滚动，正值表示向下滚动
            - duration: 每次滚动的间隔时间，默认为 0.5 秒
        """
        script = f"window.scrollBy(0, {pixels});"
        current_scroll = 0
        while current_scroll < 50:  # 设定一个滚动的上限值，可以根据需要调整
            self.driver.execute_script(script)
            current_scroll += abs(pixels)
            time.sleep(duration)

    def scroll_down(self, pixels):
        # 使用 JavaScript 执行滚动操作，滚动到指定像素数
        script = f"window.scrollBy(0, {pixels});"
        self.driver.execute_script(script)

    def scroll_up(self, pixels):
        # 使用 JavaScript 执行滚动操作，滚动到指定像素数
        script = f"window.scrollBy(0, -{pixels});"
        self.driver.execute_script(script)

    def set_proxy(self, proxy):
        if hasattr(self, 'driver'):
            self.driver.close()
            print("正在切换到代理"+proxy)
            self.options.add_argument(f'--proxy-server={proxy}')
            self.driver = webdriver.Chrome(options=self.options,service=self.service)
        else:
            print("Error")

    def clear_proxy(self):
        if hasattr(self, 'driver'):
            self.driver.close()
            self.options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=self.options,service=self.service)

if __name__ == "__main__":
    # 测试示例
    custom_driver = CustomWebDriver(
        headless=True,
        user_agent=None,  # 使用默认的 User-Agent
        proxy_server=None  # 使用默认的代理服务器
    )
    from random_proxy import proxy
    proxy_ip = proxy()
    print(proxy_ip)
    #106.14.255.124:80
    # http://httpbin.org/get
    
    custom_driver.set_proxy(proxy_ip)
    custom_driver.navigate("https://www.baidu.com")
    print(custom_driver.get_page_source())
    
    # page_soure = custom_driver.get_page_source()
    # print(page_soure)
    # 暂停 5 秒以便查看
    # import time
    # time.sleep(2)
    # input('quit? ')
    custom_driver.quit()
