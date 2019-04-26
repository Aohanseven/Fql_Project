from selenium import webdriver
import unittest
import requests
import time
import re
import json

def get_token():
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    data = {
        "corpid": 'ww1bfe0036f1ec1e74',
        "corpsecret": '-92Yv4C7KaU4AUeDRm1SoRxQy44mVTQKZj6lxZfp5lA'

    }
    r = requests.get(url=url, params=data, verify=False)
    token = r.json()['access_token']
    return token


def send_msg(token,content):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
    data = {
        "touser": '@all',                                # 企业号中的用户帐号，账号名
        "msgtype": "text",                               # 消息类型。
        "agentid": '1000026',                              # 企业号中的应用id。
        "text": {
            "content": content
        },
        "safe": "0"
    }
    r = requests.post(url=url, data=json.dumps(data), verify=False)
    return r.text




def get_web():
    r = requests.get('http://fangqianli.com')
    return r.status_code


def login(browser):
    browser = browser
    browser.find_element_by_xpath('//*[@id="DengL"]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="username"]').send_keys('16608940910')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="psw"]').send_keys('a2577811')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="loginbtn"]').click()
    time.sleep(2)
    if browser.find_element_by_link_text('16608940910'):
        return 0
    else:
        return 1


def ai_select(browser):
    browser = browser
    browser.find_element_by_xpath('//*[@id="DengL"]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="username"]').send_keys('16608940910')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="psw"]').send_keys('a2577811')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="loginbtn"]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/a').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div/div/button').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[1]/ul[1]/li[3]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[1]/ul[2]/li[2]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[4]/button[1]').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[5]/div[1]/div[1]/ul/li[1]/span').click()
    time.sleep(1)
    now_windows = browser.current_window_handle
    all_windows = browser.window_handles
    for i in all_windows:
        if i != now_windows:
            browser.switch_to_window(i)
    browser.find_element_by_xpath('//*[@id="mapBox"]/div[4]/div[2]/button').click()
    time.sleep(1)
    all_windows = browser.window_handles
    browser.switch_to_window(all_windows[2])
    time.sleep(3)
    is_ok = ''
    for i in browser.find_elements_by_xpath('//*[@id="app"]/div[2]/section[3]/div[1]/div/div/div[1]'):
        if i.is_displayed()==False:
            is_ok = 1
            break
        else:
            is_ok = 0
    return is_ok


class TestFql(unittest.TestCase):

    def test_get_web(self):
        self.assertEqual(200, get_web(), msg="主页无法访问")

    def setUp(self):
        self.opt = webdriver.ChromeOptions()
        self.opt.set_headless()
        self.browser = webdriver.Chrome('C:/Users/Administrator/Downloads/chromedriver.exe')
        self.browser.implicitly_wait(30)  # 隐性等待时间为30秒
        self.browser.get('http://fangqianli.com')

    def test_login(self):
        self.assertEqual(0, login(self.browser), msg="登录系统错误")

    def test_ai_select(self):
        self.assertEqual(0, ai_select(self.browser), msg="选址功能出错")

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":

    runner = unittest.TextTestRunner()
    testunit = unittest.TestSuite()
    testunit.addTest(TestFql("test_get_web"))
    testunit.addTest(TestFql("test_login"))
    testunit.addTest(TestFql("test_ai_select"))
    result = runner.run(testunit)
    failures = result.failures
    msg = []
    if failures != []:
        for i, k in zip(failures,range(len(failures))):
            msg.append('错误{:d}:'.format(k+1) + re.search('msg=\"(.*?)\"', i[1]).group(1))
    if msg != []:
        content = ','.join(msg)
        token = get_token()
        send_msg(token, content)