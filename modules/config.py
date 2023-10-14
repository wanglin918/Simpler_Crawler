import os
import configparser


def read_Default_config():
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建相对路径
    config_file = os.path.join(current_dir, "..", 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file,encoding='utf-8')
    #print(config.sections)
    headless_mode = config['Default'].getboolean('headless')
    load_images = int(config['Default']['image'])

    return headless_mode, load_images

def read_spider_config():
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建相对路径
    config_file = os.path.join(current_dir, "..", 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file,encoding='utf-8')
    #print(config.sections)
    headless_mode, load_images = read_Default_config()
    page_count = int(config['spider']['page'])
    keywords = config['spider']['keywords']
    return headless_mode, load_images, page_count,keywords

def read_proxy_config():

    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建相对路径
    config_file = os.path.join(current_dir, "..", 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file,encoding='utf-8')
    #print(config.sections)
    headless_mode, load_images = read_Default_config()
    proxies_num = int(config['proxypool']['proxies_num'])
    max_retries = int(config['proxypool']['max_retries'])
    return headless_mode, load_images, proxies_num, max_retries

if __name__ == "__main__":

    headless, images, pages,keywords = read_spider_config()
    print("Headless Mode:", headless)
    print("Load Images:", images)
    print("Page Count:", pages)
    print("Keyword:",keywords)

    headless, images, proxies_num, max_retries = read_proxy_config()
    print("Headless Mode:", headless)
    print("Load Images:", images)
    print(proxies_num)
    print(max_retries)
