import pymysql
import pandas as pd
import re


def chenge_content():
    con = pymysql.connect(host='192.168.0.252', user='web_user', passwd='first2018pl,', db='FBDdata2', charset='utf8', port=3306)
    sql1 = "SELECT id,content FROM News WHERE is_rep = 0 and image_urls != ''"
    sql2 = 'SELECT new_image_url,image_url FROM news_image'
    df1 = pd.read_sql(sql1, con)
    df2 = pd.read_sql(sql2,con)
    for content,id in zip(df1['content'].get_values(),df1['id'].get_values()):
        for image_url,new_image_url in zip(df2['image_url'].get_values(),df2['new_image_url'].get_values()):
            while re.findall(str(image_url),content):
                t1 = '<img src="' + image_url +'"'
                t2 = '<img class="lazy" data-original="' + new_image_url +'"'
                content = content.replace(t1,t2)
        id = id
        sql = "UPDATE News SET content='%s',is_rep=1 WHERE id=%s" % (pymysql.escape_string(content),id)
        cur = con.cursor()
        cur.execute(sql)
        print("update success %s content" % id)
        con.commit()
    con.close()


if __name__ == '__main__':
    chenge_content()