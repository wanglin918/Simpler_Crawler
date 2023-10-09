import os
import configparser


def read_config(file_path):
    
    config = configparser.ConfigParser()
    config.read(file_path,encoding='utf-8')
    print(config.sections)
    headless_mode = config['spider'].getboolean('headless')
    load_images = int(config['spider']['image'])
    page_count = int(config['spider']['page'])
    keywords = config['spider']['keywords']
    return headless_mode, load_images, page_count,keywords

if __name__ == "__main__":
    # 在这里可以添加一些测试代码，以确保配置读取函数的正确性
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建相对路径
    config_file = os.path.join(current_dir, 'config.ini')
    headless, images, pages,keywords = read_config(config_file)
    print("Headless Mode:", headless)
    print("Load Images:", images)
    print("Page Count:", pages)
    print("Keyword:",keywords)
