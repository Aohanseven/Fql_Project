import pandas as pd
import pymysql
import os


class Download_image:
    def __init__(self, startid, endid):
        self.con = pymysql.connect(
            host='192.168.0.252',
            user='web_user',
            passwd='first2018pl,',
            port=3306,
            db='FBDdata2',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.startid = startid
        self.endid = endid

    def get_info(self):
        sql = 'select id,img_id,img_order from apartment_img where id>={0} and id<={1}'.format(
            str(self.startid), str(self.endid))
        df = pd.read_sql(sql, self.con)
        urls = set(df['img_id'].tolist())
        return urls

    def download_img(self):
        urls = self.get_info()
        for url in urls:
            data_path = "D:/apartment_img/" + url + "/"
            images_path = data_path
            if os.path.isdir(images_path):
                continue
            else:
                os.makedirs(images_path)
                sql = 'select img from apartment_img where img_id = "{}"'.format(
                    url)
                df1 = pd.read_sql(sql, self.con)
                imgs = df1['img'].tolist()
                print('正在下载房源id为{}的图片'.format(url))
                for img, i in zip(imgs, range(len(imgs))):
                    image_name = images_path + str(i) + ".jpg"
                    with open(image_name, 'wb') as f:
                        f.write(img)


if __name__ == "__main__":
    start = input('请输入起始id:')
    end = input('请输入结束id:')
    Download_image(start, end).download_img()
