import pymysql
import pandas as pd
from math import *


con = pymysql.connect(host = '192.168.0.252', user = 'web_user' ,db='FBDdata2', password = 'first2018pl,',port =3306,charset='utf8')
cur = con.cursor()
def get_dis(lon1, lat1, lon2, lat2, distance):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)计算两点之间的大圆距离地球上(以十进制表示)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    dis = c * r * 1000
    if (dis <= distance):
        ok = [int(dis),1]
        return  ok
    else:
        return False


"""
lon 中心点经度 lat  中心点纬度 
lon_p 比较点经度  lat_p 比较点纬度
"""


def geo_filter(lon, lat, lon_p, lat_p, lot_lat, distance):
    if (lon_p < lon - lot_lat):
        return False
    if (lon_p > lon + lot_lat):
        return False
    if (lat_p < lat - lot_lat):
        return False
    if (lat_p > lat + lot_lat):
        return False
    return get_dis(lon, lat, lon_p, lat_p, distance)

def get_storelist():
    df1 = pd.read_sql("SELECT store_id,geo  from store_count_street_point WHERE is_street = 1",con)
    df2 = pd.read_sql("SELECT unit_rent,lat,lng  from zu_shop_data_copy_copy WHERE is_ture = 1",con)
    for store_id,geo in zip(df1['store_id'],df1['geo']):
        lat_lng = geo.split(",")
        lat = float(lat_lng[0])
        lng = float(lat_lng[1])
        rent_list = []
        for unit_rent, lat_p, lng_p, in zip(df2['unit_rent'],df2['lat'],df2['lng']):
            dis = geo_filter(lng,lat,lng_p,lat_p,0.0033,300)
            if dis != False:
                rent =  str(unit_rent) + ':' + str(dis[0])
                rent_list.append(rent)
        rent_list = (','.join(rent_list))
        cur.execute("insert into street_rent_list(store_id,geo,rent_list) VALUES ('%s','%s','%s')" % (store_id,geo,rent_list))
        print('sucess id(%s)' % store_id)
        con.commit()
    con.close()

def get_storelist1():
        df1 = pd.read_sql("SELECT store_id,geo  from street_rent_list_copy WHERE  rent_list=''", con)
        df2 = pd.read_sql("SELECT unit_rent,lat,lng  from zu_shop_data_copy_copy WHERE is_ture = 1", con)
        for store_id, geo in zip(df1['store_id'], df1['geo']):
            lat_lng = geo.split(",")
            lat = float(lat_lng[0])
            lng = float(lat_lng[1])
            rent_list = []
            for unit_rent, lat_p, lng_p, in zip(df2['unit_rent'], df2['lat'], df2['lng']):
                dis = geo_filter(lng, lat, lng_p, lat_p, 0.0105, 1000)
                if dis != False:
                    rent = str(unit_rent) + ':' + str(dis[0])
                    rent_list.append(rent)
            rent_list = (','.join(rent_list))
            cur.execute("update street_rent_list_copy set rent_list = '%s' WHERE store_id='%s'" %(rent_list,store_id))
            print('sucess id(%s)' % store_id)
            con.commit()
        con.close()
if __name__ == "__main__":
    get_storelist1()