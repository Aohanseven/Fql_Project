import pymysql
import  redis
import pandas as pd

con = pymysql.connect(host='192.168.0.252', user='web_user', passwd='first2018pl,', db='FBDdata2', charset='utf8',
                      port=3306)
df = pd.read_sql('select id from anjuke_shop_data_copy1 where is_ok=1 and monthly_rent >5000 ',con)

r=redis.Redis(host='localhost',port=6379,db=0)
redis_dict = 'fqlzu_id'
for i in df['id']:
    r.sadd(redis_dict,i)