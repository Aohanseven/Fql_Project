from selenium import webbrowser
import os, time, re, random
import pymysql, redis
from bs4 import BeautifulSoup
from selenium.webbrowser.support import expected_conditions as EC
from selenium.webbrowser.support.ui import WebbrowserWait
from selenium.webbrowser.common.by import By

image_path = ''


def get_login_page(username,password):
    # 浏览器驱动
    global browser
    opt = webbrowser.ChromeOptions()
    opt.set_headless()
    browser = webbrowser.Chrome('C:/Users/Administrator/Downloads/chromebrowser.exe',)

    # 数据获取
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
    id1 = bytes.decode(r.spop(redis_data_dict_1))

    cursor = con.cursor()
    sql = 'select * from fbd_store WHERE id=%s' % id1
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        global title
        title = result['title']
        global  acreage
        acreage = str(int(result['acreage']))
        global total_price
        total_price = str(int(result['total_price']))
        global width
        width = result['width'].strip('m')
        if width == '未填写'or '':
            width = '1'
        else:
            width = width
        global depth
        depth = result['depth'].strip('m')
        if depth == '未填写'or '':
            depth = '1'
        else:
            depth = depth
        global height
        height = result['height'].strip('m')
        if height == '未填写'or '':
            height = '1'
        else:
            height = height
        address = result['address'].split(' ')
        global region
        region = address[0].strip('区')
        global local
        local = address[1]
        global store_status
        store_status = result['store_status']
        global pic_urls
        pic_urls = result['pic_urls'].split(",")
        global image_path
        image_path = "/home/tim/Pictures/" + id1 + "/"
        os.makedirs(image_path)
        for image_id in pic_urls:
            image_name = image_path+image_id+".jpg"
            sql = 'select img from pic_info WHERE id=%s' % image_id
            cursor.execute(sql)
            img = cursor.fetchone()
            with open(image_name,'wb') as f:
                f.write(img['img'])
        global date
        date = result['date'].split('-')
        global floor
        if re.findall(r'共\d层', result['floor']):
            floor = re.findall(r'共(\d)层', result['floor'])
        else:
            floor = '1'
        content = result['intro']
        re_phone = re.compile(r'\d{11}')
        if re.search(re_phone, content) != None:
            print(re.search(re_phone, content).group())
            content = content.replace(str(re.search(re_phone, content).group()), '')
        content = content.replace('联系我时，请说是在58同城上看到的，谢谢！','')
        # keyword = ["位于","顾问"]
        # for i in keyword:
        #     i = "<span[\s\S.].*" + i + "[\s\S.].*</span>"
        #     if re.search(i, content) != None:
        #         print(re.search(i, content).group())
        #         content = content.replace(re.search(i, content).group(), '')
        global intro
        intro = content
    except Exception as e:
        print(e)
    else:
        login(username,password)
# 登录
def login(username,password):
    if browser:
        try:
            print("-----------------------------------------------------------")
            browser.get('http://vip.anjuke.com/login/?errmsg=%E7%94%A8%E6%88%B7%E5%90%8D%E5%AF%86%E7%A0%81%E9%94%99%E8%AF%AF')
            print('登录页面请求成功')
        except:
            print('登录页面请求失败')
            time.sleep(2)
            print('正在重新请求页面')

# 登录页面
    try:
        print("-----------------------------------------------------------")
        print('正在输入账号.....')
        browser.find_element_by_xpath('//*[@id="loginName"]').send_keys(username)
        print('您的账号为%s' % username)
        time.sleep(1)
        print('正在输入密码.....')
        browser.find_element_by_xpath('//*[@id="loginPwd"]').send_keys(password)
        print('您的密码为%s' % password)
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="loginSubmit"]').click()
        print('正在登录......')
        time.sleep(1)
        print('登录成功')
    except Exception as e:
        print('登录失败')
        print(e)
        time.sleep(1)
        browser.quit()

# 进入发布页面
    browser.find_element_by_xpath('//*[@id="qualification_check"]/div[1]/a').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="broker_nav"]/li[7]/a').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="broker_nav"]/li[7]/dl/dt[1]/a').click()
    time.sleep(2)
    home_page = browser.current_window_handle
    windowhanles = browser.window_handles
    for handle in windowhanles:
        if handle != home_page:
            browser.switch_to.window(handle)

# 发布信息
    locator = (By.XPATH, '//*[@id="choose"]/div[2]')
    WebbrowserWait(browser, 30, 1).until(EC.presence_of_element_located(locator))
    try:
        print("-----------------------------------------------------------")
        print('正在选择商业地产类型')
        for i in range(5):
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="chooseWebForm"]/div[1]/label[2]').click()
            if True:
                break
        print("商业地产类型为%s" %         browser.find_element_by_xpath('//*[@id="chooseWebForm"]/div[1]/label[2]').text)
    except Exception as e :
        print("##############################################")
        print('出现错误：%s' %e)
        print("##############################################")

    time.sleep(2)
    try:
        for i in range(5):
            print("-----------------------------------------------------------")
            print('正在确认操作')
            browser.find_element_by_xpath('//*[@id="chooseWebFormCommiter"]').click()
            if True:
                print('确认成功')
    except Exception as e:
        print("##############################################")
        print('出现错误：%s' % e)
        print("##############################################")

    time.sleep(2)
    try:
        print("-----------------------------------------------------------")
        print('正在选择租售方式')
        browser.find_element_by_xpath('//*[@id="jp-sale"]').click()
        print('选择租售方式为出售')
    except Exception as e:
        print("##############################################")
        print('出现错误：%s' % e)
        print("##############################################")
        time.sleep(2)
        for i in range(5):
            time.sleep(1)
            print('正在第%s重新选择' %(i+1))
            browser.find_element_by_xpath('//*[@id="jp-sale"]').click()
            if True:
                break

    time.sleep(2)
    if browser.find_elements_by_xpath('//*[@id="select-jpType"]/div/div'):
        try:
            print("-----------------------------------------------------------")
            print('正在进入商铺类型选择')
            browser.find_element_by_xpath('//*[@id="select-jpType"]/div/div').click()
            print('进入成功')
        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            time.sleep(2)
            for i in range(5):
                time.sleep(1)
                print('正在第%s次重新进入' % (i+1))
                browser.find_element_by_xpath('//*[@id="select-jpType"]/div/div').click()
                if True:
                    break

        time.sleep(2)
        try:
            print("-----------------------------------------------------------")
            print('正在选择商铺类型')
            browser.find_element_by_xpath('//*[@id="select-jpType"]/div/ul/li[4]').click()
            print('选择商铺类型为社区底商')
        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            time.sleep(2)
            for i in range(5):
                time.sleep(1)
                print('正在第%s重新选择' %(i+1))
                browser.find_element_by_xpath('//*[@id="select-jpType"]/div/ul/li[4]').click()
                if True:
                    break

        time.sleep(2)
        try:
            print("-----------------------------------------------------------")
            print('正在进入58商铺性质选择')
            browser.find_element_by_xpath('//*[@id="select-jpProperty"]/div/div').click()
            print('进入成功')
        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            for i in range(5):
                time.sleep(2)
                print('正在第%s次重新进入' % (i+1))
                browser.find_element_by_xpath('//*[@id="select-jpProperty"]/div/div').click()
                if True:
                    print("重新选择成功")
                    break

        time.sleep(2)
        try:
            print("-----------------------------------------------------------")
            print('正在选择商铺性质')
            browser.find_element_by_xpath('//*[@id="select-jpProperty"]/div/ul/li[3]').click()
            print('选择商铺性质为商铺新房')
        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            for i in range(5):
                time.sleep(2)
                print('正在第%s次重新进入' %(i+1))
                browser.find_element_by_xpath('//*[@id="select-jpProperty"]/div/ul/li[3]').click()
                if True:
                    break

    time.sleep(1)
# 商铺所在层数
    browser.find_element_by_name('startFloor').send_keys('1')
    time.sleep(1)
# 总层数
    browser.find_element_by_name('totalFloor').send_keys(floor)
    time.sleep(1)
# 总面积
    browser.find_element_by_name('roomarea').send_keys(acreage)
    time.sleep(1)
# 面宽
    browser.find_element_by_name('faceWidth').send_keys(width)
    time.sleep(1)
# 层高
    browser.find_element_by_name('floorHigh').send_keys(height)
    time.sleep(1)
# 进深
    browser.find_element_by_name('spatialDepth').send_keys(depth)
    time.sleep(1)

    for i in browser.find_elements_by_name('fitment[]'):
        time.sleep(0.5)
        i.click()

    for i in (browser.find_elements_by_name('customer[]')[:3]):
        time.sleep(0.5)
        i.click()

    time.sleep(1)
    browser.find_element_by_partial_link_text('是').click()


    time.sleep(3)
    if browser.find_elements_by_xpath('//*[@id="ajk-jp-input"]'):
        try:
            print("-----------------------------------------------------------")
            print('正在填写安居客地址')
            print("-----------------------------------------------------------")

            browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').send_keys(local)
            time.sleep(5)
            if browser.find_elements_by_xpath('//*[@id="publish_form"]/div[13]/div/ul/li'):
                print('填写地址为：%s' % (local))
            else:
                browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').clear()
                browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').send_keys(region)
                browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').click()
                time.sleep(3)
                if browser.find_elements_by_xpath('//*[@id="publish_form"]/div[13]/div/ul/li'):
                    print('填写地址为：%s' % region)

        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            for i in range(5):
                print('正在第%s次重新填写' % (i+1))
                browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').clear()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').send_keys(region)
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').send_keys(local)
                time.sleep(1)
                if browser.find_elements_by_xpath('//*[@id="publish_form"]/div[13]/div/ul/li'):
                    browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').click()
                    print('填写地址为：%s' % (region+local))
                else:
                    browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').clear()
                    browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').send_keys(region)
                    print('填写地址为：%s' % region)
                    if True:
                        print('填写成功')
                        break

        time.sleep(2)
        try:
            # browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').click()
            print("-----------------------------------------------------------")
            print('正在选择安居客地址')
            print("-----------------------------------------------------------")
            # time.sleep(2)
            # browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').click()
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="publish_form"]/div[13]/div/ul/li[%s]' % (random.randint(1,len(browser.find_elements_by_xpath('//*[@id="publish_form"]/div[13]/div/ul/li'))))).click()
        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            for i in range(5):
                time.sleep(2)
                print('正在第%s次重新选择' % (i+1))
                browser.find_element_by_xpath('//*[@id="detail_address58"]').click()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="ajk-jp-input"]').click()
                time.sleep(3)
                browser.find_element_by_xpath('//*[@id="publish_form"]/div[13]/div/ul/li[%s]' % (random.randint(1,len(browser.find_elements_by_xpath('//*[@id="publish_form"]/div[13]/div/ul/li'))))).click()
                if True:
                    print('选择成功')
                    break
        try:
            browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/div').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="select-blockAJK"]/div/div').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/div').click()
            try:
                f = browser.find_elements_by_xpath('//*[@id="select-zoneAJK"]/div/ul/li')
                for i in f:
                    if i.text == region:
                        print('安居客区域为：%s' % region)
                        i.click()
                # browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/ul/li[8]').click()
            except:
                browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/div').click()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="select-blockAJK"]/div/div').click()
                time.sleep(1)
                browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/div').click()
                time.sleep(1)
                f = browser.find_elements_by_xpath('//*[@id="select-zoneAJK"]/div/ul/li')
                for i in range(5):
                    print('正在第%s重新选择' % (i+1))
                    for i in f:
                        if i.text == region:
                            print('安居客区域为：%s' % region)
                            i.click()
                    browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/ul/li[8]').click()
        except:
            print('无此选项')

        try:
            browser.find_element_by_xpath('//*[@id="select-blockAJK"]/div/div').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/div').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="select-blockAJK"]/div/div').click()
            time.sleep(1)
            try:
                f = browser.find_elements_by_xpath('//*[@id="select-blockAJK"]/div/ul/li')
                for i in f:
                    if i.text == local:
                        print('安居客地点为：%s' % local)
                        i.click()
                # browser.find_element_by_xpath('//*[@id="select-blockGJ"]/div/ul/li[1]').click()
            except:
                browser.find_element_by_xpath('//*[@id="select-blockAJK"]/div/div').click()
                browser.find_element_by_xpath('//*[@id="select-blockAJK"]/div/div').click()
                f = browser.find_elements_by_xpath('//*[@id="select-blockAJK"]/div/ul/li')
                for i in range(5):
                    print('正在第%s重新选择' % (i+1))
                    for i in f:
                        if i.text == region:
                            print('安居客区域为：%s' % local)
                            i.click()
                    # browser.find_element_by_xpath('//*[@id="select-zoneAJK"]/div/ul/li[8]').click()
        except:
            print('无此选项')
# 58位置信息
    if browser.find_elements_by_xpath('//*[@id="detail_address58"]'):
        try:
            print("-----------------------------------------------------------")
            print('正在填写58地址')
            browser.find_element_by_xpath('//*[@id="detail_address58"]').send_keys(region)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="detail_address58"]').send_keys(local)
            time.sleep(3)
            if browser.find_elements_by_xpath('//*[@id="publish_form"]/div[16]/div/ul/li'):
                print('填写地址为：%s' % (region+local))
            else:
                browser.find_element_by_xpath('//*[@id="detail_address58"]').clear()
                browser.find_element_by_xpath('//*[@id="detail_address58"]').send_keys(local)
                browser.find_element_by_xpath('//*[@id="detail_address58"]').click()
        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            for i in range(1,5):
                print('正在第%s次重新填写' % i)
                browser.find_element_by_xpath('//*[@id="detail_address58"]').clear()
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="detail_address58"]').send_keys(local)
                if True:
                    print('填写成功')
                    break

        try:
            time.sleep(3)
            print("-----------------------------------------------------------")
            print('正在选择58地址')
            locator = (By.XPATH, '//*[@id="publish_form"]/div[16]/div/ul/li')
            WebbrowserWait(browser,10,1).until(EC.presence_of_all_elements_located(locator))
            browser.find_element_by_xpath('//*[@id="publish_form"]/div[16]/div/ul/li[%s]' % random.randint(1, len(browser.find_elements_by_xpath('//*[@id="publish_form"]/div[16]/div/ul/li')))).click()
        except Exception as e:
            print("##############################################")
            print('出现错误：%s' % e)
            print("##############################################")
            for i  in range(5):
                time.sleep(2)
                print('正在第%s次重新选择' % (i+1))
                browser.find_element_by_xpath('//*[@id="detail_address58"]').click()
                time.sleep(2)
                locator = (By.XPATH, '//*[@id="publish_form"]/div[16]/div/ul/li')
                WebbrowserWait(browser, 10, 1).until(EC.presence_of_all_elements_located(locator))
                browser.find_element_by_xpath('//*[@id="publish_form"]/div[16]/div/ul/li[%s]' % random.randint(1, len(browser.find_elements_by_xpath('//*[@id="publish_form"]/div[16]/div/ul/li')))).click()
                if True:
                    print('选择成功')
                    break
# 58区域选择
        try:
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="select-zone58"]/div/div').click()
            time.sleep(2)
            f = browser.find_elements_by_xpath('//*[@id="select-zone58"]/div/ul/li')
            time.sleep(1)
            for i in f:
                if i.text == region:
                    print('58区域为：%s' % region)
                    i.click()
                    break
                elif i.text == (region + "区"):
                    print('58区域为：%s' % region)
                    i.click()
        except Exception as e:
            print(e)
            for i in range(5):
                print('正在第%s次从选择')
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="select-zone58"]/div/div').click()
                time.sleep(2)
                f = browser.find_elements_by_xpath('//*[@id="select-zone58"]/div/ul/li')
                time.sleep(1)
                for i in f:
                    if i.text == region:
                        print('58区域为：%s' % region)
                        i.click()
                        if True:
                            break
                    elif i.text == (region + "区"):
                        print('58区域：%s' % region)
                        i.click()
        try:
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="select-block58"]/div/div').click()
            time.sleep(2)
            f = browser.find_elements_by_xpath('//*[@id="select-block58"]/div/ul/li')
            time.sleep(1)
            for i in f:
                if i.text == local:
                    print('58地点为：%s' % local)
                    i.click()
                    break
        except Exception as e:
            print(e)
            for i in range(5):
                print('正在第%s次从选择')
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="select-block58"]/div/div').click()
                time.sleep(2)
                f = browser.find_elements_by_xpath('//*[@id="select-block58"]/div/ul/li')
                time.sleep(1)
                for i in f:
                    if i.text == local:
                        print('58地点为：%s' % local)
                        i.click()
                        if True:
                            break

# 价格
    browser.find_element_by_xpath('//*[@id="saleprice-box-c"]/input').send_keys(total_price)
# 文章标题内容
    print("正在输入文章内容")
    browser.find_element_by_name('title').send_keys(title)
    time.sleep(1)
    shop = BeautifulSoup(intro, 'html.parser')
    content = shop.find('div').get_text()
    browser.switch_to_frame(browser.find_element_by_xpath('//*[@id="editor-wrap"]/div[2]/div/div[2]/iframe').send_keys(content))
    time.sleep(1)

# 房屋图片
    for i in os.listdir(image_path):
        try:
            image = image_path + i
            browser.find_element_by_name('file').send_keys(image)
            time.sleep(1)
        except:
            browser.find_element_by_xpath('//*[@id="alert"]/div[2]/a').click()

    for j in range(1,len(browser.find_elements_by_xpath('//*[@id="pic-upload-display"]/div'))):
        if j < 5:
            browser.find_element_by_xpath('//*[@id="pic-upload-display"]/div[%d]/div[1]/select/option[%d]' % (j, j + 1)).click()
        else:
            browser.find_element_by_xpath('//*[@id="pic-upload-display"]/div[%d]/div[1]/select/option[%d]' % (j, 4)).click()
    browser.find_element_by_xpath('//*[@id="pic-upload-display"]/div[%s]/div[2]/i[1]' % (random.randint(1, j))).click()

    # try:
    #     for i , j in zip(os.listdir(image_path),range(1,(len(os.listdir(image_path)))+1)):
    #         print("正在上传第%s张图片" % j)
    #         if  j < 5 :
    #             image = image_path+ i
    #             browser.find_element_by_name('file').send_keys(image)
    #             time.sleep(1)
    #             # if browser.find_element_by_xpath('//*[@id="alert"]/div[2]/a'):
    #             #     browser.find_element_by_xpath('//*[@id="alert"]/div[2]/a').click()
    #             browser.find_element_by_xpath('//*[@id="pic-upload-display"]/div[%d]/div[1]/select/option[%d]'% (j,j+1)).click()
    #             time.sleep(1)
    #         else:
    #             image = image_path + i
    #             browser.find_element_by_name('file').send_keys(image)
    #             time.sleep(1)
    #             # if browser.find_element_by_xpath('//*[@id="alert"]/div[2]/a'):
    #             #     browser.find_element_by_xpath('//*[@id="alert"]/div[2]/a').click()
    #             browser.find_element_by_xpath('//*[@id="pic-upload-display"]/div[%d]/div[1]/select/option[%d]' % (j, 4)).click()
    #             time.sleep(1)
    #     browser.find_element_by_xpath('//*[@id="pic-upload-display"]/div[%s]/div[2]/i[1]' % (random.randint(1,j))).click()
    # except Exception as e:
    time.sleep(3)
    try:
        browser.find_element_by_xpath('//*[@id="publish-jpshop-add"]').click()
        time.sleep(2)

    finally:
        browser.quit()
        print('成功发送本条房源')


if __name__ == '__main__':
    get_login_page()
