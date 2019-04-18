import pymysql
import redis
import pandas as pd

con = pymysql.connect(
    host='211.149.228.56',
    user='root',
    passwd='firstdb123',
    port=3306,
    db='firstdb',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

r = redis.Redis(host='localhost', port=6379)
redis_data_dict_1 = "unused_id"
sql = "SELECT id FROM fbd_store"
df = pd.read_sql(sql, con)

for id in df['id'].tolist():
    r.sadd(redis_data_dict_1, id)
    print('%s加入去重队列', id)





