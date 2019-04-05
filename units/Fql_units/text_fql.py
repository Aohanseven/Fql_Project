from selenium import webdriver
from HtmlTestRunner import HTMLTestRunner
import unittest
import requests
import time

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
        return True
    else:
        return False


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
    for i in browser.find_elements_by_xpath('//*[@id="app"]/div[2]/section[3]/div[1]/div/div/div[1]'):
        if i.is_displayed()==False:
            is_ok = 0
            break
        else:
            is_ok = 1

    return is_ok


class TestFql(unittest.TestCase):

    def test_get_web(self):
        self.assertEqual(200, get_web())

    def setUp(self):
        self.opt = webdriver.ChromeOptions()
        self.opt.set_headless()
        self.browser = webdriver.Chrome('C:/Users/Administrator/Downloads/chromedriver.exe',options=self.opt)
        self.browser.implicitly_wait(30)  # 隐性等待时间为30秒
        self.browser.get('http://fangqianli.com')

    def test_login(self):
        self.assertTrue(login(self.browser))

    def test_ai_select(self):
        self.assertEqual(1, ai_select(self.browser))

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    testunit = unittest.TestSuite()

    testunit.addTest(TestFql("test_get_web"))

    testunit.addTest(TestFql("test_login"))

    testunit.addTest(TestFql("test_ai_select"))

    HtmlFile = "E:/Fql_Project/units/HTML_test/report.html"

    fp = open(HtmlFile, "wb")

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='房千里测试报告',
        description='用例执行情况：'
        )

    runner.run(testunit)

    fp.close()