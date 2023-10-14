import random
from database_manager import DatabaseManager

def proxy():

    proxy_list = []

    sql = DatabaseManager()

    results = sql.select_ip_port_from_proxypool()

    for row in results:

        ip, port = row

        proxy_url = "http://{}:{}".format(ip, port)

        proxy_list.append(proxy_url)

        
    proxy_url = random.choice(proxy_list)

    print("正在使用的代理:"+proxy_url)

    #print(type(proxy_url))

    return proxy_url

if __name__ == "__main__":

    proxy()