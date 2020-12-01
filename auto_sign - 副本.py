import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from splinter import Browser
from selenium.webdriver.support import expected_conditions as EC

url = "https://newids.seu.edu.cn/authserver/login?" \
      "service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp2%2Fsys%2FlwReportEpidemicSeu%2Findex.do%3Ft_s%3D1583630260225#/dailyReport"

option=webdriver.ChromeOptions()
#option.add_argument('headless') 
broswer = webdriver.Chrome(chrome_options=option) 

def login():
    broswer.get(url)
    broswer.find_element_by_id("username").send_keys("your username")
    broswer.find_element_by_id("password").send_keys("your password")
    broswer.find_element_by_class_name("auth_login_btn").click()
def add():

    element = WebDriverWait(broswer, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="emapdatatable"]'))
    )

    broswer.find_element_by_xpath('//*[@data-action="add"]').click()

    element = WebDriverWait(broswer, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@name="DZ_JSDTCJTW"]'))
    )

    tiwen=[36.5,36.6,36.7]
    broswer.find_element_by_name("DZ_JSDTCJTW").clear()
    broswer.find_element_by_name("DZ_JSDTCJTW").send_keys(str(random.choice(tiwen)))

    broswer.find_element_by_id('save').click()

    broswer.find_element_by_xpath("//*[text()='确认']").click()


login()
add()