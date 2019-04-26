# -*- coding: utf-8 -*- 
import itchat
import re
import pymysql
import datetime
import emoji
newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=True)
def save_info(come_from,msg):
    try:
#         print("=========")
        msg = msg.replace(":", "qwer")
        msg =str(emoji.demojize(str(msg)))
        msg = re.sub("(:.*?:)", '', msg)
        msg=msg.replace("qwer",":")
        msg=msg.replace("line_space","\n")
        print("save"+msg)
        conn = pymysql.connect(host='211.149.228.56', user='root', password='firstdb123', database='firstdb',charset='utf8mb4')
        cue = conn.cursor()
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO qun_info(come_from,info,date_time) VALUES ('%s','%s','%s')" % (come_from,msg,date_time)
        cue.execute(sql)
        conn.commit()
    except Exception as e:
        send_erramsg()
        print(e)
    finally:
        conn.close()
        
def send_erramsg():
    uname = newInstance.search_friends(name="严杰") 
    newInstance.send_msg("微信发送失败",uname[0]["UserName"]) 
    
        
@newInstance.msg_register(itchat.content.TEXT, itchat.content.isGroupChat=True)
def reply(msg):
    msg = str(dict(msg)['Content'])
    msg =str(emoji.demojize(str(msg)))
    msg = re.sub("(:.*?:)", '', msg)
    msg=msg.replace("qwer",":").replace("(Text)","")
    msg=msg.replace('\n','line_space')
    if re.match(".*房发现.*收客时间.*",msg):
        msg=re.search("房发现.*",msg).group()
        
#         msg=msg.replace(":","qwer")
        save_info("房发现",msg)
    elif re.match(".*安居客.*收客时间.*", msg):
#         print("come in ")
        msg = re.search("安居客.*", msg).group()
#         msg = msg.replace(":", "qwer")
        save_info("安居客",msg)
    elif re.match(".*58.*收客时间.*", msg):
        msg = re.search("58.*", msg).group()
#         msg = msg.replace(":", "qwer")
        save_info("58",msg)
    elif re.match(".*赶集.*收客时间.*", msg):
        msg = re.search("赶集.*", msg).group()
#         msg = msg.replace(":", "qwer")
        save_info("赶集",msg)

newInstance.run()