import pandas as pd
import pymysql


def get_info():
    con = pymysql.connect(
        host='192.168.0.252',
        user='web_user',
        passwd='first2018pl,',
        port=3306,
        db='FBDdata2',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    sql = 'select id,img_id,img_order from apartment_img where id<1000'
    df1 = pd.read_sql(sql,con)
    urls = set(df1['img_id'].tolist())
    return urls


def download_imge():
    urls = get_info()
    sql = 'select max(img_order) from apartment_img where id = "%s"'
    for url in urls:
        df1 = pd.read_sql(sql, con)


if __name__ == "__main__":
    get_info()