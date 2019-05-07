import requests
from lxml import etree
import pymysql
import re
import multiprocessing
import time

class Ajkapartment:

    def __init__(self, i):
        self.host = '192.168.0.252'
        self.user = 'web_user'
        self.passwd = 'first2018pl,'
        self.db = 'FBDdata2'
        self.charset = 'utf8'
        self.port = 3306
        self.home_url = "http://cd.sp.anjuke.com/shou/p%s/?kw=公寓" % str(i)
        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'accept-language',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }

    def insert_image(self, img, img_id, order, con):
        cue = con.cursor()
        try:
            cue.execute(
                'insert into ajk_apartment_image(img,img_id,img_order) values (%s,%s,%s)',
                (img,
                 img_id,
                 order))
            print("Insert success")
        except Exception as e:
            print("Insert error:", e)
            con.rollback()
        else:
            con.commit()

    def get_urls(self):
        req = requests.get(self.home_url, headers=self.header).text
        selector = etree.HTML(req)
        urls = selector.xpath('//*[@id="list-content"]/div/@link')
        return urls

    def get_img(self):
        self.con = pymysql.connect(host=self.host,
                                   user=self.user,
                                   passwd=self.passwd,
                                   db=self.db,
                                   charset=self.charset,
                                   port=self.port)
        urls = self.get_urls()
        for url in urls:
            time.sleep(4)
            req = requests.get(url, headers=self.header)
            imgurls = re.findall(
                r'<img data-lazy="(.*?)" alt="">',req.text)
            img_id = re.search(
                r'http://cd.sp.anjuke.com/shou/(.*)/\?pt=.*', url).group(1)
            if imgurls != []:
                for imgurl, order in zip(imgurls, range(1, len(imgurls))):
                    try:
                        img = requests.get(imgurl).content
                    except BaseException:
                        continue
                    else:
                        self.insert_image(
                            img=img, img_id=img_id, order=order, con=self.con)
        self.con.close()


if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=4)
    for i in range(1, 60):
        print('正在爬取第%s页' % i)
        pool.apply_async(Ajkapartment(i).get_img())
    pool.close()
    pool.join()
