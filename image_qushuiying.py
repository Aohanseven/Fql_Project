# -*- coding: utf-8 -*-

import os, time
import threadpool
from nowatermark import  WatermarkRemover
import pymysql

def Handle_image(image):
    remover = WatermarkRemover()
    remover.load_watermark_template(watermark_template_filename)
    remover.remove_watermark(no_path + image, ok_path + image)
    #os.remove(no_path + image)

if __name__ == '__main__':
    while True:
        boo = False
        if time.localtime().tm_hour == 2:
            boo = True
        no_path = '/home/tim/image_no'
        ok_path = '/home/tim/image_ok'
        watermark_template_filename = '/home/tim/Desktop/template.jpg'
        images = os.listdir(no_path)
        start = time.time()
        task_pool = threadpool.ThreadPool(10)
        requests = threadpool.makeRequests(Handle_image,images)
        count = 0
        for req in requests:
            try:
                count+=1
                task_pool.putRequest(req)
                print('正在处理第%s张' % count)
            except:
                print('出现错误')
        task_pool.wait()
        end = time.time()
        print('用时%s' %str(end-start))
        if boo:
            con = pymysql.connect(host='192.168.0.252', user='root', passwd='123456', db='FBDdata2', charset='utf8',
                                 port=3306)
            cue = con.cursor()
            cue.execute("INSERT INTO  dianpu_image(type,add_time) VALUES(%s,%s)",(2,time.strftime("%Y-%m-%d",time.localtime())))
            con.commit()
            con.close()
        time.sleep(3600)


