import os
import requests
import redis
import time


def get_ip():
    redis_db = redis.Redis(host='127.0.0.1', port=6379, db=9)
    while True:
        orders = ["0f95da88048caaa92a1a2dd703db9794", '229fe5fcc9902d1deb61ed09162db48c']
        Apiurls = ["http://api.ip.data5u.com/dynamic/get.html?order=" + order for order in orders]
        ips = [requests.get(apiUrl).content.decode().strip() for apiUrl in Apiurls]
        for ip in ips:
            if ip != 'too many requests':
                redis_db.setex(ip, 30, 0)
        print(ips)
        time.sleep(10)


if __name__ == '__main__':
    get_ip()
