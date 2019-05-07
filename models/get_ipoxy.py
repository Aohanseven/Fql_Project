import threading
import redis
import requests
import time


def get_ipoxy(order):
    s = requests.session()
    redis_db = redis.Redis(host='127.0.0.1', port=6379, db=9)
    while True:
        apiurl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
        try:
            ip = s.get(apiurl).text.strip()
            if ip != 'too many requests':
                redis_db.setex(ip, 30, 0)
                print(ip)
                time.sleep(6)
        except BaseException:
            ip = s.get(apiurl).text.strip()
            if ip != 'too many requests':
                redis_db.setex(ip, 30, 0)
                print(ip)
                time.sleep(6)


if __name__ == '__main__':

    t1 = threading.Thread(
        target=get_ipoxy, args=(
            "0f95da88048caaa92a1a2dd703db9794",))
    t2 = threading.Thread(
        target=get_ipoxy, args=(
            "229fe5fcc9902d1deb61ed09162db48c",))
    t1.start()
    t2.start()
