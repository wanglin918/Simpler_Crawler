from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# # 获取当前安装的 Chrome WebDriver 版本
# installed_version = ChromeDriverManager().get_installed_version()
# print("当前安装的 Chrome WebDriver 版本是:", installed_version)
#print(os.getcwd())
# 获取最新的 Chrome WebDriver 版本
driver_path = ChromeDriverManager().install()
print(driver_path)

# 创建Chrome WebDriver，并指定驱动路径
driver = webdriver.Chrome()
# 打开百度网页
driver.get("https://www.baidu.com")
driver.quit()
