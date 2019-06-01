import re
import time
import random
import requests
import pymysql


def get_image():
    for i in range(1, 6):
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%88%BF%E4%BA%A7%E6%94%BF%E7%AD%96%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%88%BF%E4%BA%A7%E6%94%BF%E7%AD%96%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=' + \
            str(i * 30) + '&rn=30&gsm=5a&1531799417573='
        req = requests.get(url).text

        urls = re.findall('"thumbURL":"(.*?)"', req)
        print(req)
        print(urls)
        for url in urls:
            if url != '':
                image_url = url
                image_type = 2
                image = requests.get(image_url).content
                new_image_url = 'http://fbd.fangqianli.com/FBDweb/News_pic?img=' + \
                    str(int(time.time())) + str(random.randint(1000, 9999)) + '.img'
                id = re.findall(
                    r'http://fbd.fangqianli.com/FBDweb/News_pic\?img=(.*?)\..*',
                    new_image_url)[0]
                conn = pymysql.connect(
                    host='192.168.0.252',
                    user='web_user',
                    passwd='first2018pl,',
                    db='FBDdata2',
                    charset='utf8',
                    port=3306)
                cue = conn.cursor()
                print('mysql connect success')
                try:
                    cue.execute(
                        "INSERT INTO news_image(id,image,image_url,new_image_url,image_type) VALUES (%s,%s,%s,%s,%s)",
                        (id,
                         image,
                         image_url,
                         new_image_url,
                         image_type))
                    print("Insert success")
                except BaseException:
                    print("Insert error:")
                    conn.rollback()
                else:
                    conn.commit()
                conn.close()


if __name__ == '__main__':
    get_image()
