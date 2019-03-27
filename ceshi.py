import requests
import pandas as pd
import pymysql
import re
import time
import random



def get_image():
    con = pymysql.connect(host='192.168.0.252', user='root', passwd='123456', db='FBDdata2', charset='utf8', port=3306)
    sql = "SELECT content FROM News"
    df = pd.read_sql(sql, con)
    for link in df['content'].get_values():
        image_urls = re.findall(r'<img\ssrc="(https://.*?)"',link)
        if image_urls :
            for url in image_urls:
                image = requests.get(url).content
                image_url = url
                new_image_url = 'http://fangfaxian.iego.cn/FBDweb/News_pic?img=' + str(int(time.time())) + str(random.randint(1000, 9999)) + '.img'
                id = re.findall(r'http://fangfaxian\.iego\.cn/FBDweb/News_pic\?img=(.*?)\..*',new_image_url)[0]
                image_type = 1
                conn = pymysql.connect(host='192.168.0.252', user='root', passwd='123456', db='FBDdata2', charset='utf8',port=3306)
                cue = conn.cursor()
                print('mysql connect success')
                try:
                    cue.execute("INSERT INTO news_image(id,image,image_url,new_image_url,image_type) VALUES (%s,%s,%s,%s,%s)",(id,image,image_url,new_image_url,image_type) )
                    print("Insert success")
                except:
                    print("Insert error:")
                    conn.rollback()
                else:
                    conn.commit()
                conn.close()




if __name__ == '__main__':
    get_image()

