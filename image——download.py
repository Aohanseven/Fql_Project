import pymysql
import os
import pandas as pd
from nowatermark import WatermarkRemover


def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
        f.close()


def Handle_image(image_no_path,image_ok_path):
    remover = WatermarkRemover()
    remover.load_watermark_template('C:/Users/Administrator/Desktop/template.png')
    remover.remove_watermark(image_no_path, image_ok_path)


if __name__ == '__main__':
    while True:
        select_id = input("请输入需要下载的房源图片ID:")
        con = pymysql.connect(host='192.168.0.252', user='web_user', passwd='first2018pl,', db='FBDdata2', charset='utf8',
                              port=3306)
        cue = con.cursor()
        try:
            cue.execute("select id,image_urls from anjuke_shop_data_copy1 where is_ok = 1 and id = '%s'" % select_id )
        except:
            print('房源id有误请重新输入')
        data = cue.fetchone()
        shop_id = data[0]
        image_urls = data[1].split(',')
        path = 'C:/Users/Administrator/Desktop/fql_images/'
        if os.path.exists(path) == False:
            os.mkdir(path)
        shop_path = path + shop_id +'/'
        no_path = shop_path + 'is_no/'
        ok_path = shop_path + 'is_ok/'
        if os.path.exists(shop_path) == False:
            os.mkdir(shop_path)
            os.mkdir(no_path)
            os.mkdir(ok_path)
        for image_id in image_urls:
            image_no_path = no_path + image_id + ".jpg"
            image_ok_path = ok_path + image_id + ".jpg"
            cue.execute("select image from fqlzu_image where image_id= '%s'" % str(image_id))
            image = cue.fetchone()[0]
            write_file(image, image_no_path)
            Handle_image(image_no_path,image_ok_path)
        print('下载成功')