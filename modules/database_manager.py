# -*- coding: UTF-8 -*-

import sqlite3
from sqlite3 import Error
import os
class DatabaseManager:
    def __init__(self):
        # 定义数据库文件的名称
        spider_db = "spider.db"
        proxypool_db = "proxypool.db"

        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建相对路径，拼接数据库文件的完整路径
        self.spider_db = os.path.join(current_dir, "..", r'database\{}').format(spider_db)
        self.proxypool_db = os.path.join(current_dir, "..", r'database\{}').format(proxypool_db)

    def create_spider_table(self):
        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.spider_db)
            print("数据库连接成功")

            # 创建名为result的数据表，如果不存在的话
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS result
                              (title TEXT,
                               site TEXT,
                               link TEXT,
                               url TEXT DEFAULT NULL,
                               have_url INTEGER DEFAULT 0,
                               is_test INTEGER DEFAULT 0,
                               vul INTEGER DEFAULT 0)''')
            
            # 提交事务，保存更改
            conn.commit()
            
            # 关闭数据库连接
            conn.close()
        except Error as e:
            print(e)

    def create_proxypool_table(self):
        try:
            # 连接到proxypool_db数据库
            conn = sqlite3.connect(self.proxypool_db)
            print("数据库连接成功")

            # 创建名为proxypool的数据表，如果不存在的话
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS proxypool
                              (ip TEXT UNIQUE,
                               port TEXT,
                               level TEXT,
                               type TEXT,
                               speed TEXT,
                               lasttime TEXT,
                               is_useful INTEGER DEFAULT 0)''')
            
            # 提交事务，保存更改
            conn.commit()
            
            # 关闭数据库连接
            conn.close()
        except Error as e:
            print(e)

    def insert_into_result(self, title, site, link, url=None, have_url=0, is_test=0, vul=0):
        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.spider_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 检查是否已经存在相同的 title 和 site
            cursor.execute("SELECT * FROM result WHERE title = ? AND site = ?", (title, site))
            existing = cursor.fetchone()

            # 如果没有重复的记录，就插入新记录
            if not existing:
                cursor.execute("INSERT OR IGNORE INTO result VALUES (?, ?, ?, ?, ?, ?, ?)", (title, site, link, url, have_url, is_test, vul))
                conn.commit()
                print("数据成功插入")
            else:
                print("数据已重复")
            
            # 关闭数据库连接
            conn.close()
        except Error as e:
            print(e)

    def delete_from_result(self):
        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.spider_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 删除符合条件的记录
            cursor.execute("DELETE FROM result WHERE is_test = 1 AND vul = 0")
            
            # 提交事务，保存更改
            conn.commit()
            
            print("数据删除成功")

            # 关闭数据库连接
            conn.close()
        except Error as e:
            print(e)

    def select_links_from_result(self):
        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.spider_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 查询所有符合条件的记录的链接
            cursor.execute("SELECT link FROM result WHERE have_url = 0")
            
            # 获取查询结果中的所有链接
            links = [row[0] for row in cursor.fetchall()]

            # 关闭数据库连接
            conn.close()
            
            print("链接查询成功")
            return links
        except Error as e:
            print(e)
            return []

    def update_urls_in_result(self, new_url, old_link):
        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.spider_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 更新链接为指定值的记录的URL
            cursor.execute("UPDATE result SET url = ?, have_url = ? WHERE link = ?", (new_url, 1, old_link))

            
            # 提交事务，保存更改
            conn.commit()

            # 关闭数据库连接
            conn.close()
            
            print("URL更改成功")
        except Error as e:
            print(e)

    def select_urls_from_result(self):
        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.spider_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 查询所有符合条件的记录的URL
            cursor.execute("SELECT url FROM result WHERE is_test = 0")
            
            # 获取查询结果中的所有URL
            urls = [row[0] for row in cursor.fetchall()]

            # 关闭数据库连接
            conn.close()
            
            print("URL查询成功")
            return urls
        except Error as e:
            print(e)
            return []

    def insert_into_proxypool(self, ip, port, level, type, speed, lasttime, is_useful=0):
        try:
            # 连接到proxypool_db数据库
            conn = sqlite3.connect(self.proxypool_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 检查是否已经存在相同的 IP 和 Port
            cursor.execute("SELECT * FROM proxypool WHERE ip = ? AND port = ?", (ip, port))
            existing = cursor.fetchone()

            # 如果没有重复的记录，就插入新记录
            if not existing:
                cursor.execute("INSERT OR IGNORE INTO proxypool VALUES (?, ?, ?, ?, ?, ?, 0)", (ip, port, level, type, speed, lasttime))
                conn.commit()
                print("数据插入成功")
            else:
                print("数据已重复")

            # 关闭数据库连接
            conn.close()
        except Error as e:
            print(e)

    def select_ip_port_from_proxypool(self):
        try:
            # 连接到proxypool_db数据库
            conn = sqlite3.connect(self.proxypool_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 查询所有记录的 IP 和 Port
            cursor.execute("SELECT ip, port FROM proxypool")
            
            # 获取查询结果中的所有 IP 和 Port
            results = cursor.fetchall()

            # 关闭数据库连接
            conn.close()
            print("IP 和 Port 查询成功")
            return results
        except Error as e:
            print(e)
            return []


    def delete_ip_from_proxypool(self, ip):
        try:
            # 连接到proxypool_db数据库
            conn = sqlite3.connect(self.proxypool_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 删除符合条件的记录
            cursor.execute("DELETE FROM proxypool WHERE ip = ?", (ip,))
            
            # 提交事务，保存更改
            conn.commit()
            
            print("IP 删除成功")

            # 关闭数据库连接
            conn.close()
        except Error as e:
            print(e)

    def update_proxypool(self, ip):
        try:
            # 连接到proxypool_db数据库
            conn = sqlite3.connect(self.proxypool_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 更新 is_useful 到指定值的记录
            cursor.execute("UPDATE proxypool SET is_useful = 1 WHERE ip = ?", (ip,))
            
            # 提交事务，保存更改
            conn.commit()
            
            print("is_useful 更改成功")

            # 关闭数据库连接
            conn.close()
        except Error as e:
            print(e)

    def select_proxypool_and_result(self):
        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.spider_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 查询所有符合条件的记录的 URL
            cursor.execute("SELECT url FROM result WHERE have_url = 0")
            
            # 获取查询结果中的所有 URL
            result_urls = [row[0] for row in cursor.fetchall()]

            # 关闭数据库连接
            conn.close()

            # 再次连接到proxypool_db数据库
            conn = sqlite3.connect(self.proxypool_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 查询所有记录的 IP 和 Port
            cursor.execute("SELECT ip, port FROM proxypool")
            
            # 获取查询结果中的所有 IP 和 Port
            proxypool_ips = cursor.fetchall()

            # 关闭数据库连接
            conn.close()
            
            print("URL, IP 和 Port 查询成功")
            return proxypool_ips, result_urls
        except Error as e:
            print(e)
            return [], []
    
    def select_proxypool_num(self):

        try:
            # 连接到spider_db数据库
            conn = sqlite3.connect(self.proxypool_db)
            
            # 创建游标
            cursor = conn.cursor()

            # 查询所有符合条件的记录的 URL
            cursor.execute("SELECT count(*) FROM proxypool")

            result = cursor.fetchone()[0]

            print("proxypool共有{}条记录".format(result))

            cursor.close()

            # 关闭数据库连接
            conn.close()

            print(result)
            return result
        
        except Error as e:
            print(e)

if __name__ == "__main__":
    

    sql = DatabaseManager()

    # sql.create_spider_table()
    # sql.insert_into_result('test','test','test',None,0,0,0)
    # sql.create_proxypool_table()
    # sql.insert_into_proxypool("58.220.95.55","9400","高匿名","HTTP","0.3秒","2023-10-10 14:31:01",1)
    # sql.insert_into_proxypool("58.220.95.54","9400","高匿名","HTTP","0.2秒","2023-10-10 10:31:01",1)
    # sql.insert_into_proxypool("58.220.95.79","10000","高匿名","HTTP","0.2秒","2023-10-10 07:31:01",1)
    # sql.delete_ip_from_proxypool("192.168.1.1")
    #
    # sql.select_proxypool_num()
    # sql.select_ip_port_from_proxypool()
    # sql.select_links_from_result()
    results = sql.select_links_from_result()
    for row in results:
        print(row)
