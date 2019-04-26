# -*- coding: utf-8 -*- 
import re
import itchat
from rediscluster import  StrictRedisCluster
newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=True,statusStorageDir='newInstance.pkl')
import time
import traceback
redis_nodes =[{'host':'192.168.0.251','port':6379}, 
{'host':'192.168.0.247','port':6379}, 
{'host':'192.168.0.254','port':6379}, 
{'host':'192.168.0.252','port':6379}, 
{'host':'192.168.0.253','port':6379}, 
{'host':'192.168.0.248','port':6379}, 
] 
r = StrictRedisCluster(startup_nodes=redis_nodes,decode_responses=True)

def send_msg(room_name,info):
    try:
       
        newInstance.get_chatrooms(update=True)
        iRoom = newInstance.search_chatrooms(room_name) 
        for room in iRoom:
            if room_name in room['NickName']:
                userName = room['UserName']
                break
        if len(iRoom)==0:
            return 0
        newInstance.send_msg(info, userName) 
        print("发送成功"+room_name)
        return 1
    except Exception as e :
        traceback.print_exc()
        return 0
def send_erramsg():
    try:
    	uname = newInstance.search_friends(name="严杰") 
    	newInstance.send_msg("微信发送失败",uname[0]["UserName"]) 
    except Exception as e :
        traceback.print_exc()
    
    
ex_count=0
while True:
    try:
        if ex_count>10:
            send_erramsg()
            break
        time.sleep(10)
        content = r.lpop("ak")
#         print(content)
        if not content:
#             print("meiyoushuju ")
            continue
        else:
            reObject=re.search("(.*?)&&(.*)",content)
            if reObject:
                department= reObject.group(1).lstrip('"')
                info=reObject.group(2).rstrip('"')
                print(department,info)
                status =send_msg(department,info)
                if status==0:
                    ex_count+=1
                    r.rpush('ak',reObject)
    except Exception as e:
        traceback.print_exc()
        ex_count+=1
    
