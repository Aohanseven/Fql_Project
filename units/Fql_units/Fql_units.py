from selenium import webdriver
import unittest
import requests
import time


def get_web():
    r = requests.get('http://fangqianli.com')
    return r.status_code

def login():
    browser = webdriver.Chrome('C:/Users/Administrator/Downloads/chromedriver.exe')
    browser.get('http://fangqianli.com')
    browser.find_elements_by_xpath('//*[@id="DengL"]').click()
    browser.find_elements_by_xpath('//*[@id="username"]').send_keys('16608940910')
    browser.find_elements_by_xpath('//*[@id="psw"]').send_keys('a2577811')
    browser.find_elements_by_xpath('//*[@id="loginbtn"]').click()
    username = browser.find_elements_by_xpath('//*[@id="DengL"]/text()')
    return username


class TestFql(unittest.TestCase):

    def test_get_web(self):
        self.assertEqual(200, get_web())

    def test_login(self):
        self.assertEqual('16608940910', login())

if __name__=='__main__':
    unittest.main()
