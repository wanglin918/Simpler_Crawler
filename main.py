import sys
sys.path.append(".\modules")

# 导入你的模块或函数
from modules import spider
from modules import link_test
from modules import proxy

def run_spider():
    spider.baidu_spider()

def get_url_from_link():
    link_test.test()

def get_and_check_proxy():
    proxy.proxy_spider()

if __name__ == "__main__":
    while True:
        print("请选择要运行的功能:")
        print("1. 运行爬虫")
        print("2. 获取并检查代理")
        print("3. 获取链接并检查")
        print("4. 退出")

        choice = input("请输入选项 (1/2/3/4): ")

        if choice == '1':
            run_spider()
        elif choice == '2':
            get_and_check_proxy()
        elif choice == '3':
            get_url_from_link()
        elif choice == '4':
            print("退出程序")
            break
        else:
            print("无效选项，请重新输入。")
