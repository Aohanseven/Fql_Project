import requests
from lxml import etree
import pymysql
import hashlib
import multiprocessing


class Apartment:

    def __init__(self, i):
        self.host = '192.168.0.252'
        self.user = 'web_user'
        self.passwd = 'first2018pl,'
        self.db = 'FBDdata2'
        self.charset = 'utf8'
        self.port = 3306
        self.home_url = "https://cd.58.com/pinpaigongyu/pn/%s/?from=ajkp_home_zf_daohang_ppgy_wwl&logofrom=anjuke&segment=true&encryptData=d_5friq6cZIP9akIYyRs-_uNmbJ2hNbhnPshc1vE1zK0zh2CQ07Ei-kEZa2_JkZeIBxUxtbIyiP_AoNgfYk7zq8bNnUJ9jCwz3cH2KDpMNHNxe0mNWCdrudAMOW_B-0R" % i
        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'accept-language',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }

#   字符串转为MD5值
    def str_md5(self, src):
        my_sha = hashlib.sha1()
        my_sha.update(str(src).encode('utf-8'))
        my_sha_Digest = my_sha.hexdigest()
        return my_sha_Digest

    def insert_image(self, img, img_id, order, con):
        cue = con.cursor()
        try:
            cue.execute(
                'insert into apartment_img(img,img_id,img_order) values (%s,%s,%s)', (img, img_id, order))
            print("Insert success")
        except Exception as e:
            print("Insert error:", e)
            con.rollback()
        else:
            con.commit()

    def get_urls(self):
        req = requests.get(self.home_url, headers=self.header).text
        selector = etree.HTML(req)
        urls = selector.xpath('/html/body/div[5]/ul/li/a/@href')
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
            req = requests.get(url, headers=self.header)
            selector = etree.HTML(req.text)
            imgurls = selector.xpath('//*[@id="pic-list"]/li/img/@lazy_src')
            img_id = str(self.str_md5(url))[16:]
            if imgurls != []:
                for imgurl, order in zip(imgurls, range(1, len(imgurls))):
                    try:
                        img = requests.get('http:' + imgurl).content
                    except:
                        continue
                    else:
                        self.insert_image(img=img, img_id=img_id, order=order, con=self.con)
        self.con.close()


if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=4)
    for i in range(1, 170):
        print('正在爬取第%s页'% i)
        # Apartment(i).get_img()
        pool.apply_async(Apartment(i).get_img())
    #
    pool.close()
    pool.join()
