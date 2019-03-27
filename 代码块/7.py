#!/usr/bin/env python
# -* - coding: UTF-8 -* -

from io import StringIO
import math
from random import randrange
import random
import re
import time
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
    from PIL import Image
from selenium import webbrowser
from selenium.webbrowser.common.action_chains import ActionChains
from selenium.webbrowser.common.by import By
from selenium.webbrowser.common.desired_capabilities import DesiredCapabilities
from selenium.webbrowser.support import expected_conditions as EC
from selenium.webbrowser.support.ui import WebbrowserWait


host = '192.168.1.253'
user = 'root'
pwd  = 'suitang$$zt##*ASD'   # to be modified.
table   = 'suitang'

class IndustryAndCommerceGeetestCrack(): 

    def __init__(self,
                 sql_id,
                 sql_money,
                 url,
                 search_text,
                 input_id='keyword',
                 search_element_id='btn_query',
                 gt_element_class_name='gt_box',
                 gt_close_class_name='gt_popup_cross',
                 gt_slider_knob_name='gt_slider_knob',
                 result_numbers_xpath='//*[@id="searchtipsu1"]/p/span[2]',
                 result_list_verify_id=None,
                 result_list_verify_class=None,
                 is_gap_every_broad=True):

        """
        url: 主页面的地址
        search_text: 搜索企业名称
        input_id: 输入框网页元素id
        search_element_id: 查询按钮网页元素id
        gt_element_class_name: 滑块验证码图片元素的class类名，基本一样，在调用时可以不传参
        gt_slider_knob_name: 滑块验证码图片拖动元素的class类名，基本一样，在调用时可以不传参
        result_numbers_xpath: 用于确认是否搜索成功的 搜索结果数量的xpath,如本次搜索共`50`条结果，用时多少秒
        result_list_verify_id: 搜索结果列表一项的某个标签id值，用于确认搜索列表已经加载完成(某些网站使用ajax) or
        result_list_verify_class: 搜索结果列表一项的某个标签class类名，用于确认搜索列表已经加载完成(某些网站使用ajax)
        is_gap_every_broad: 现在已经确定为True值，是为了兼容湖北等省原先滑块小的问题，现在网站已经更改，调用时可以忽略此参数了
        """
        try:
            self.id =sql_id
            self.money = sql_money
            self.url = url
            self.search_text = search_text
            self.input_id = input_id
            self.search_element_id = search_element_id
            self.gt_element_class_name = gt_element_class_name
            self.gt_close_class_name = gt_close_class_name;
            self.gt_slider_knob_name = gt_slider_knob_name
            self.result_numbers_xpath = result_numbers_xpath
            self.result_list_verify_id = result_list_verify_id
            self.result_list_verify_class = result_list_verify_class
            self.is_gap_every_broad = is_gap_every_broad
            
            
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
            )
            #C:\\soft\\chromebrowser_win32\\chromebrowser.exe
            #self.browser = webbrowser.PhantomJS("E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe",desired_capabilities=dcap)
            #self.browser = webbrowser.Chrome("C:\\Windows\\browsers\\chrome\\chromebrowser.exe")
            self.browser = webbrowser.Chrome("C:\\browsers\\chrome\\chromebrowser.exe")
            
            self.browser.maximize_window()
            time.sleep(random.uniform(1.0, 1.5))
        except:
            print "启动浏览器失败。重新启动"
    def get_search_page(self,
                        url="http://www.gsxt.gov.cn/index.html",
                        search_text=u"中国移动",
                        input_id=u"keyword",
                        search_element_id='btn_query',
                        gt_element_class_name="gt_box"):

        """点击查询按钮
            :search_text: Unicode, 要输入的文本
            :input_id: 输入框网页元素id
            :search_element_id: 查询按钮网页元素id
            :gt_element_class_name: 验证码图片网页元素class名
        """
    #    while count_load<1:
            # 根据页面进入主页面，并等待搜索框id出现
        try:
            self.browser.set_script_timeout(20)
            self.browser.get(url)
            wait = WebbrowserWait(self.browser, 20)
            element = wait.until(EC.presence_of_element_located((By.ID, input_id)))
            time.sleep(random.uniform(2.0, 3.0))
       
        # 清空搜索框，搜索企业，点击搜索
            element.clear()
            element.send_keys(search_text)
            element = self.browser.find_element_by_id(search_element_id)
            element.click()
            wait = WebbrowserWait(self.browser, 10)
      
            element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            gt_element_class_name)))
            time.sleep(random.uniform(0.5, 1.0))
            return 1
        except:
            return 0

    def crop_captcha_image(self, gt_element_class_name="gt_box"):

        """截取验证码图片

        :gt_element_class_name: 验证码图片网页元素id
        :returns: StringIO, 图片内容

        """
        captcha_el = self.browser.find_element_by_class_name(
            gt_element_class_name)
        location = captcha_el.location
        size = captcha_el.size
        left = int(location['x'])
        top = int(location['y'])
        right = int(location['x'] + size['width'])
        bottom = int(location['y'] + size['height'])

        screenshot = self.browser.get_screenshot_as_png()
#         print left, top, right, bottom
        screenshot = Image.open(StringIO.StringIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        # captcha.save("/Users/haijunt/%s.png" % uuid.uuid4().get_hex())
        return captcha

    # 点击刷新滑块验证码
    def click_refresh(self, sleep_time=0.6):
        element = self.browser.find_element_by_class_name('gt_refresh_button')
        element.click()
        time.sleep(sleep_time)

    def is_pixel_equal(self, img1, img2, x, y):
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        if (abs(pix1[0] - pix2[0]) < 80) and (abs(pix1[1] - pix2[1]) < 80) and (
                    abs(pix1[2] - pix2[2]) < 80):
            return True
        else:
            return False

    def calculate_slider_offset(self,
                                slide_times = 0,
                                max_slide_times = 5, 
                                gt_element_class_name="gt_box", 
                                is_gap_every_broad=True):

        """计算滑块偏移位置，必须在点击查询按钮之后调用
        :slide_times: 当前滑块滑行的次数
        :max_slide_times: 滑行的最大次数
        :gt_element_class_name: 滑块元素的类名
        :is_gap_every_broad: 滑块的元素是不是非常少，原先湖北等几个省有这样情况，现在无
        :returns: Number
        """
        img1 = self.crop_captcha_image(gt_element_class_name=gt_element_class_name)
        self.drag_and_drop_test(x_offset= random.uniform(2.0, 5.0))
        img2 = self.crop_captcha_image(gt_element_class_name=gt_element_class_name)
        w1, h1 = img1.size
        w2, h2 = img2.size
        if w1 != w2 or h1 != h2:
            return False
        left = 0
        flag = False
        if is_gap_every_broad:
            x_start, distance_one, distance_two = 61, 18, 8
        else:
            x_start, distance_one, distance_two = 45, 2, 0
        for i in xrange(x_start, w1):
            for j in xrange(h1):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    flag = True
                    break
            if flag:
                break
        # 如果位置太近，选择点击刷新，重新破解
        if left == x_start and slide_times < max_slide_times:
            self.click_refresh()
            return self.calculate_slider_offset(slide_times=slide_times + 1,
                                                max_slide_times=max_slide_times,
                                                gt_element_class_name=gt_element_class_name,
                                                is_gap_every_broad=is_gap_every_broad)
        elif left == x_start and slide_times >= max_slide_times:
            left = left - distance_one
 
        else:
            left = left - distance_two
#         print u"需要划动的像素点：", left
        return left

    def drag_and_drop_test(self,
                           x_offset=0,
                           y_offset=0,
                           element_class="gt_slider_knob"):
        
        """拖拽滑块

        :x_offset: 相对滑块x坐标偏移
        :y_offset: 相对滑块y坐标偏移
        :element_class: 滑块网页元素CSS类名
        :use for: 拖拽滑块出现需要滑动的位置
        """
        dragger = self.browser.find_element_by_class_name(element_class)
        action = ActionChains(self.browser)
        action.drag_and_drop_by_offset(dragger, x_offset, y_offset).perform()
        time.sleep(2.8)

    def get_trail_array(self, distance):
        """
        :distance: 需要划动的像素点
        :return :array_trail,[(x,y,t)] 由x,y,及休息时间t组成的元组构成的列表
        """
        array_trail = []
        array_x = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
        array_xre = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
        for i in range(60):
            array_x[i] = random.uniform(0.05,0.3)
            array_xre[i] = random.uniform(0.001,0.002)
        #array_x = [1.0/3, 1.0/4, 1.0/5, 2.0/5, 1.0/6, 2.0/7, 3.0/8, 2.0/9]
        array_y = [-0.1, -0.2, -0.3, -0.4, -0.5, 0.1, 0.2, 0.3, 0.4, 0.5]
#         last_move_distance = random.choice([-3, +3, -4, +4, -5, +5, -6, +6])
#         distance = distance + last_move_distance
#         distance = distance + last_move_distance

        x = math.ceil(distance * random.choice(array_x))
        y = random.choice(array_y)
        t = random.uniform(0.02, 0.04)
        count_w = 1;
        while distance >= 2:
#             print x, y, t
            count_w +=1
            array_trail.append((x, y, t))
            distance = distance - x
            if distance == 0:
                break
            x = math.ceil(distance * random.choice(array_x))
#             y = random.choice(array_y)
            t = random.uniform(0.1, 0.4)
            rint = random.randint(0,50)
            if rint %3==0:
                y = random.uniform(-0.3,0.3)
            if count_w>3 and rint ==0:
                x = -math.ceil(distance * random.choice(array_xre))
                t = random.uniform(0.2, 0.3)

#         x = 1 if last_move_distance < 0 else -1
#         last_move_distance = abs(last_move_distance)
#         for _ in range(last_move_distance):
#             y = random.choice(array_y)
#             t = random.uniform(0.2, 0.5)
#             array_trail.append((x, y, t))

        return array_trail

    def drag_and_drop(self,
                      x_offset=0,
                      y_offset=0,
                      gt_slider_knob_name="gt_slider_knob",
                      result_numbers_xpath='/html/body/div[5]/div[3]/div[1]/span',
                      result_list_verify_id=None,
                      result_list_verify_class=None):
        """拖拽滑块

        :x_offset: 相对滑块x坐标偏移
        :y_offset: 相对滑块y坐标偏移
        :gt_slider_knob_name: 滑块网页元素CSS类名
        :result_numbers_xpath: 搜索结果数量的xpath，有些省份如贵州可能不需要
        :result_list_verify_id: 确认有搜索结果元素出现的id or
        :result_list_verify_class: 确认有搜索结果元素的class 二选一
        :Returns: crack_result
        :return 0: 搜索结果为0(搜索的企业不存在)
        :return -1: 滑动位置失败或者被怪物吃了(有机器学习反爬),但会自动进行点击刷新重新破解(最多5次)
        :return 1: 破解成功
        """

        array_trail = self.get_trail_array(x_offset)
#         for x, y, t in array_trail:
#             print x, y, t

        element = self.browser.find_element_by_class_name(gt_slider_knob_name)
        ActionChains(self.browser).click_and_hold(on_element=element).perform()
        for x, y, t in array_trail:
            ActionChains(self.browser).move_to_element_with_offset(
                to_element=element, 
                xoffset=x+22,
                yoffset=y+22).perform()
            # 这个动作在phantomjs里一定需要，否则 x 是不会移动的，phantomjs成败在此一举(chrome等忽略)
            ActionChains(self.browser).click_and_hold().perform()
            # 可以在调试的时候查看 x 是否有移动，这一点非常重要
            # temp_element = self.browser.find_element_by_class_name(gt_slider_knob_name)
            # print temp_element.location
            time.sleep(t)

        time.sleep(0.4)
#         print u'稍等一会儿，搜索结果马上出来...'
        ActionChains(self.browser).release(on_element=element).perform()

        time.sleep(0.5)
        element = u"成功"
        try:
            element = self.browser.find_element_by_class_name('gt_info_text')
            status = element.text
        except:
            status = u"成功"
       
#         print u"破解验证码的结果: ", status
        # 这个延时必须有，在滑动后等待回复原状
        if not status:
            status=u'成功'
        if status.find(u'失败') > -1:
            self.click_refresh()
            return -1
        if status.find(u'怪物') > -1:
            self.click_refresh(3.4)
            return -1
        if status.find(u'关闭') > -1:
            return -2
        wait = WebbrowserWait(self.browser, 30, 1.0)
        number = -1;
        
        try:
            wait = WebbrowserWait(self.browser, 30)
            element = wait.until(EC.presence_of_element_located((By.XPATH, result_numbers_xpath)))
            time.sleep(random.uniform(1.0, 2.0))
            number = element.text
#             print "number=%s"%number
        except:
            return -1;
        
#         print u'搜索结果数量: ', number
        if int(number) == 0:
            self.set_status() 
            print "%s==无结果"%self.search_text
            #更改状态为0 
            return 0
        else:
            wait = WebbrowserWait(self.browser,20)
            if result_list_verify_class:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, result_list_verify_class)))
                element = self.browser.find_element_by_xpath("/html/body/div[5]/div[3]/a[1]/h1")
                location = element.location
                left = int(location['x'])
                top = int(location['y'])
                x_add = randrange(10,50)+left
                y_add = randrange(10,50)+top
                ActionChains(self.browser).move_by_offset(x_add, y_add).perform()
                count_serch=1
                while count_serch<5: 
                    try :
                        element = self.browser.find_element_by_xpath("/html/body/div[5]/div[3]/a[%d]/h1"%count_serch)
                        response_name = element.text
                    except :
                        self.set_status() 
                        print "%s==无结果"%response_name
                        return  0 ;
                    if response_name == self.search_text:
                        time.sleep(1)
                        element.click()
                        self.browser.set_script_timeout(20)
                        #qyqx-detail
                        time.sleep(4)
        #                 print self.browser.page_source
                        self.browser.switch_to_window(self.browser.window_handles[1])
                        credit_code = "";company_type = "";legal="" ;capital_money = "";date_esta= "";date_close = "";
                        reg_agency= "" ;date_correct = ""; reg_status  = "";detail_address = "";business_scope = "";
                        credit_code = self.browser.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[1]/dd').text
                        company_type = self.browser.find_element_by_xpath ('//*[@id="primaryInfo"]/div/div[2]/dl[3]/dd').text
                        legal = self.browser.find_element_by_xpath ('//*[@id="primaryInfo"]/div/div[2]/dl[4]/dd').text
                        for i in range(5,14):
                            try :
                                element_name =self.browser.find_element_by_xpath ('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dt'%i).text
                                element_value = self.browser.find_element_by_xpath ('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dd'%i).text
                                if element_name.find("资本")>-1 or element_name.find("金")>-1:
                                    capital_money=element_value
                                elif element_name.find("成立")>-1:
                                    date_esta= element_value 
                                elif element_name.find("至")>-1:
                                    date_close =element_value
                                elif element_name.find("机")>-1:
                                    reg_agency = element_value
                                elif element_name.find("核")>-1:
                                    date_correct = element_value
                                elif element_name.find("状态")>-1:
                                    reg_status = element_value
                                elif element_name.find("所")>-1 or element_name.find("地")>-1:
                                    detail_address = element_value
                                elif element_name.find("范围")>-1:
                                    business_scope = element_value
                            except :
                                print "数据有部分缺失"
                                break 
                            
                        #将金额字符串做简化，省略掉后边多于的0 
                        try :
                            res = re.findall(r"\d+\.?\d*",capital_money)
                            r = res.rstrip('0').strip('.') if '.' in res else res
                            numberResult=re.search('[^0](.*)[^0]',r[0]).group()
                            if numberResult[-1]==u'.':
                                numberResult=numberResult[:-1]
                            elif numberResult[0]==u'.':
                                numberResult=u'0'+numberResult
                            capital_money = numberResult
                        except :
                            print "截取金额出错"
                        #对所有时间格式做简化,统一格式为YYYY.MM.DD             
                        try :
                            if date_esta :
                                date_esta= self.time_format(date_esta)
                            if date_close:
                                date_close=self.time_format(date_close)
                            if date_correct:
                                date_correct =self.time_format(date_correct)
                        except :
                            print "时间格式化出错"                       
                        
                        print "信用代码：%s"%credit_code
                        print "类型：%s"%company_type
                        print "法人代表：%s"%legal
                        print "注册资本金：%s"%capital_money
                        print "成立日期:%s"%date_esta
                        print "营业期限至：%s"%date_close
                        print "登记机构：%s"%reg_agency
                        print "核准日期：%s"%date_correct
                        print "登记状态：%s"%reg_status
                        print "住址：%s"%detail_address
                        print "经营范围：%s"%business_scope
                        is_insert =self.update_info( 
                                        credit_code,
                                        company_type,
                                        legal,
                                        capital_money,
                                        date_esta,
                                        date_close,
                                        reg_agency,
                                        date_correct,
                                        reg_status,
                                        detail_address,
                                        business_scope)
                        if is_insert ==1:
                            print "%s==完成"%response_name
                            return 1
                        else:
                            print "%s==失败"%response_name
                            return -2
                    else :
                        count_serch +=1          
                else :
                    self.set_status() 
                    print "%s==无结果"%response_name
                    #更改状态为0 
                    return 0 
    #格式化时间
    def time_format(self,a): 
        timeArray = time.strptime(a, u"%Y年%m月%d日")
        time_resut = time.strftime(u"%Y-%m-%d", timeArray)
        return time_resut                       
                
    #查到数据后更新数据         
    def update_info( self,
                    credit_code,
                    company_type,
                    legal,
                    capital_money,
                    date_esta,
                    date_close,
                    reg_agency,
                    date_correct,
                    reg_status,
                    detail_address,
                    business_scope
                ):
        try: 
            
            
            conn = MySQLdb.connect(host,user,pwd,table,charset='utf8')
        # 使用cursor()方法获取操作游标
            sql_id = int(self.id)
            cursor = conn.cursor()
            if capital_money!='':
                sql ="UPDATE stang_new_evaluate_intelligence set credit_code ='%s',type='%s',\
legal='%s',capital_money='%s',date_esta='%s',date_close='%s',reg_agency='%s',\
date_correct='%s',reg_status='%s',detail_address='%s',business_scope='%s',update_status= '1' where \
id=%d "%(credit_code,company_type,legal,capital_money,date_esta,date_close,reg_agency,date_correct,reg_status,detail_address,business_scope,sql_id)
            else :
                sql ="UPDATE stang_new_evaluate_intelligence set credit_code ='%s',type='%s',\
legal='%s',date_esta='%s',date_close='%s',reg_agency='%s',\
date_correct='%s',reg_status='%s',detail_address='%s',business_scope='%s',update_status= '1' where \
id=%d "%(credit_code,company_type,legal,date_esta,date_close,reg_agency,date_correct,reg_status,detail_address,business_scope,sql_id)  
            cursor.execute(sql)         
            cursor.close()
            conn.commit()
            conn.close()
            return 1
        except :
            print "====================================写入数据库出错"
    def set_status(self):
        try :
            conn = MySQLdb.connect(host,user,pwd,table,charset='utf8')
            # 使用cursor()方法获取操作游标
            sql_id = int(self.id)
            cursor = conn.cursor()
            sql = "UPDATE stang_new_evaluate_intelligence set update_status ='0' where id =%d"%sql_id
            cursor.execute(sql)         
            cursor.close()
            conn.commit()
            conn.close()
        except :
            print "==============================================修改status出错"
         
#         except :
#             return 0
                     
                
                
                
#                self.browser.switch_to_frame(element)
#                element = self.browser.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[2]/dd')
# #                 print element.text
#                 element = self.browser.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[5]/dd/text()')
# #                 print element.text
# #             elif result_list_verify_id:
# #                 element = wait.until(EC.presence_of_element_located((By.ID, result_list_verify_id)))
            #time.sleep(random.uniform(2.0, 3.0))

    def crack(self, max_crack_times=5):
        """
        max_crack_times: 最大点击刷新的数量
        Returns: 搜索结果列表的网页源代码，访问的cookies
        content == 0: 搜索结果为0(企业不存在)
        content == -1: 在破解过程中出错了，可以传参数不对，可能本身出错
        else source code
        """
        try:
            is_load=self.get_search_page(
                url=self.url,
                search_text=self.search_text,
                input_id=self.input_id,
                search_element_id=self.search_element_id,
                gt_element_class_name=self.gt_element_class_name)
            if is_load ==0:
                print "网站查询按钮加载失败，等待半分钟继续"
                time.sleep(5)
                self.browser.quit()
                return -1
            count = 0
            while count < max_crack_times:
                count += 1
                x_offset = self.calculate_slider_offset(
                    slide_times=0,
                    max_slide_times=5,
                    gt_element_class_name=self.gt_element_class_name,
                    is_gap_every_broad=self.is_gap_every_broad)
                status = self.drag_and_drop(
                    x_offset=x_offset,
                    gt_slider_knob_name=self.gt_slider_knob_name,
                    result_numbers_xpath=self.result_numbers_xpath,
                    result_list_verify_id=self.result_list_verify_id,
                    result_list_verify_class=self.result_list_verify_class)
                if status == 1 or status == 0 or status == -2:
                    self.browser.quit()
                    return status
            else:
#                 print u'验证码破解已经达到最大次数: %s' % max_crack_times
                status = -1
                self.browser.quit()
            return status
        except:
            print "出错啦！！！！！！！！！！！！"
            print traceback.print_exc()
            self.browser.quit()
            return -2


if __name__ == '__main__':
    # # 湖北
    # c = IndustryAndCommerceGeetestCrack(
    #     url="http://xyjg.egs.gov.cn/ECPS_HB/index.jspx", 
    #     search_text=u"工业大学",
    #     result_list_verify_id='gggscpnamebox')
    # print c.crack()[1]

    # 吉林
#     c = IndustryAndCommerceGeetestCrack(
#         url="http://211.141.74.198:8083/", 
#         search_text=u"工业大学",
#         input_id="txtSearch",
#         search_element_id="btnSearch",
#         gt_element_class_name="gt_box",
#         gt_slider_knob_name="gt_slider_knob",
#         result_numbers_xpath='/html/body/div[1]/div[3]/div[1]/span[2]',
#         result_list_verify_class='m-searchresult')
#     print c.crack(3)[1]

    # # 陕西
    # c = IndustryAndCommerceGeetestCrack(
    #     url="http://xygs.snaic.gov.cn/ztxy.do?method=index&random=1479870596271", 
    #     search_text=u"工业大学",
    #     input_id="entname",
    #     search_element_id="popup-submit",
    #     gt_element_class_name="gt_box",
    #     gt_slider_knob_name="gt_slider_knob",
    #     result_numbers_xpath='//*[@id="myDiv"]/p/span',
    #     result_list_verify_class='result_item')
    # print c.crack()[1]
    # /html/body/div[5]/ul/li[1]/h3
    # /html/body/div[1]/table/tbody/tr[1]/td[1]
    # /html/body/div[1]/table/tbody/tr[3]/td[1]
    
    db = MySQLdb.connect(host,user,pwd,table,charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    sql = "SELECT id,company_name,capital_money FROM stang_new_evaluate_intelligence e  \
       where e.update_status ='%s' and id>1173887  "% ("")
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        try:
            ids= row[0]
            companyname = row[1]
            money= row[2]
            count_browser = 0;
            while True :
                c = IndustryAndCommerceGeetestCrack(
                sql_id = ids,
                sql_money = money,
                url="http://www.gsxt.gov.cn/index.html", 
                search_text=companyname,
                input_id="keyword",
                search_element_id="btn_query",
                gt_element_class_name="gt_box",
                gt_close_class_name="gt_popup_cross",
                gt_slider_knob_name="gt_slider_knob",
                result_numbers_xpath='/html/body/div[5]/div[3]/div[1]/span',
                result_list_verify_class='f20')
                res =c.crack()
                if res ==1 or res ==0:
                    break
                if res ==-1 or res ==-2:
                    count_browser +=1
                    if count_browser>2:
                        c.set_status()
                        break
        except:
            print "Error: unable to fecth data"
            print traceback.print_exc()
   

    # # 河北
    # c = IndustryAndCommerceGeetestCrack(
    #     url="http://www.hebscztxyxx.gov.cn/notice/", 
    #     search_text=u"工业大学",
    #     input_id="keyword",
    #     search_element_id="buttonSearch",
    #     gt_element_class_name="gt_box",
    #     gt_slider_knob_name="gt_slider_knob",
    #     result_numbers_xpath='//*[@id="wrap1366"]/div[3]/div/div/p/span',
    #     result_list_verify_class='tableContent')
    # print c.crack()[1]

    # # 云南
    # c = IndustryAndCommerceGeetestCrack(
    #     url="http://gsxt.ynaic.gov.cn/notice/", 
    #     search_text=u"工业大学",
    #     input_id="keyword",
    #     search_element_id="buttonSearch",
    #     gt_element_class_name="gt_box",
    #     gt_slider_knob_name="gt_slider_knob",
    #     result_numbers_xpath='//*[@id="wrap1366"]/div[3]/div/div/p/span',
    #     result_list_verify_class='tableContent')
    # print c.crack()[1]

    # # 青海
    # c = IndustryAndCommerceGeetestCrack(
    #     url='http://218.95.241.36/index.jspx',
    #     search_text=u'中国移动',
    #     input_id='searchText',
    #     search_element_id='click',
    #     gt_element_class_name='gt_box',
    #     gt_slider_knob_name='gt_slider_knob',
    #     result_numbers_xpath='//*[@id="searchtipsu1"]/p/span[2]',
    #     result_list_verify_id='gggscpnametext',
    #     result_list_verify_class=None,
    #     is_gap_every_broad=True)
    # content, cookies = c.crack()
    # print cookies

