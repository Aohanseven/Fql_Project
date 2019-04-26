import itchat


newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=True)


@newInstance.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isGroupChat=True)
# 使用装饰器注册print_content函数，TEXT表示为文本信息
def reply(msg):
    print(msg)


newInstance.run()