import random
import time

def random_sleep(start, end):
        t = random.uniform(start, end)
        print("随机暂停{}秒".format(t))
        time.sleep(t)

if __name__ == "__main__":
    random_sleep(1,2)