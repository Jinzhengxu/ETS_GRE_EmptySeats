33# -*- coding: utf-8 -*
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fateadm_api import *
from info import *
from email.mime.text import MIMEText
from corpwechatbot.app import AppMsgSender
import pandas as pd
import csv
import urllib
import schedule
import smtplib
import pyperclip
import pyautogui
import time
import logging
import os

logging.basicConfig(filename='Program-log.txt',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)
logging.debug('Start of program.')
logging.info('The main mould is working.')
pyautogui.FAILSAFE = False

def sign_in(user):
    msg=1
    api = FateadmApi(app_id, app_key, pd_id, pd_key)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=options)
    with open("./stealth.min.js/stealth.min.js") as f:
        js = f.read()
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
        })

    browser.get('https://gre.neea.cn/')
    time.sleep(10)
    logging.info("Successfully get chrome driver.")
    flag=1
    
    while(flag):
        rsp = signproc(api)
        flag = checklogin()            
        if flag:
            pyautogui.moveTo(270, 450)
            pyautogui.click()
            api.Justice(rsp.request_id)

    time.sleep(5)
    if flag==0:
        print("lets find seats")
        pyautogui.click()
        pyautogui.moveTo(790,420)
        pyautogui.click()
        time.sleep(3)
        pyautogui.moveTo(194,672)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(775,676)
        pyautogui.click()
        time.sleep(3)
    selectcity()
    saveweb()
    checkseats()

    browser.quit()
    return 1;

def checkseats():
    msg = []
    have = 0
    tb = pd.read_html('../Downloads/data.html')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    city = [[],[],[],[],[]]
    city[0] = tb[2]
    city[1] = tb[4]
    city[2] = tb[6]
    city[3] = tb[8]
    city[4] = tb[10]
    for i in city:
        #print(i)
        for index,row in i.iterrows():
            #print(index)
            print(row[0])
            if row[3] == "有":
                have = 1
                msg.append(row[0]+row[1]+"，终于有空位了hxd")

    if have == 1:
        for i in msg:
            #mail(i, user.email1, 1)
            sms(i)
    else:
        nothave = "还是没有空位啊hxd"
        #mail(nothave, user.email1, 0)
    logging.info("Emailing to User {0} for notification".format(user.uid))

    
def saveweb():
    clc(370,158)
    pyautogui.rightClick()
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite('data')
    pyautogui.press('enter')
    time.sleep(2)
    clc(700,474)
    
def signproc(api):
    pyautogui.typewrite(user.uid, interval=0.25)
    pyautogui.press('enter')
    pyautogui.typewrite(user.pwd, interval=0.25)
    pyautogui.press('enter')
    time.sleep(3)
    #action = ActionChains(browser)
    pyautogui.moveTo(300, 550)
    pyautogui.rightClick()
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')

    src = pyperclip.paste()
    while(True):
        rsp = captcha_pred(src, api)
        if rsp.ret_code == 0:
            break
    
    pyautogui.moveTo(300, 580)
    pyautogui.click()
    pyautogui.typewrite(rsp.pred_rsp.value, interval=0.25)
    #pyautogui.typewrite("cnmb", interval=0.25)
    pyautogui.press('enter')
    time.sleep(5)
    return rsp
    
def checklogin():
    pyautogui.moveTo(250, 420)
    pyautogui.dragRel(80,0, duration=0.5)
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.click()
    string = pyperclip.paste()
    #print(string)
    if string == "验证码不正确":
        return 1
    else:
        return 0
    return 0

def selectcity():
    clc(299,499)
    clc(325,530)
    clc(299,569)
    clc(319,536)
    clc(322,559)
    clc(301,595)
    clc(316,561)
    clc(330,583)
    clc(301,624)
    clc(316,505)
    clc(294,532)
    clc(311,645)
    clc(297,682)
    clc(364,684)
    clc(432,684)
    clc(498,686)
    clc(331,592)
    clc(563,626)
    clc(674,449)
    #----
    #clc(554,492)
    #time.sleep(1)
    #clc(516,594)
    #----
    clc(692,533)

def clc(x,y):
    pyautogui.moveTo(x,y)
    pyautogui.click()
    time.sleep(1)
    
def captcha_pred(url, api):
    #识别类型， 具体类型可以查看官方网站的价格页选择具体的类型
    pred_type = "20400"
    # 查询余额
    balance = api.QueryBalcExtend()   # 直接返余额
    # 如果不是通过文件识别，则调用Predict接口：
    # result = api.PredictExtend(pred_type,data)       # 直接返回识别结果
    img = urllib.request.urlopen(url)
    data = img.read()
    rsp = api.Predict(pred_type,data)  # 返回详细的识别结果
    return rsp;

def mail(mail_text, mail_to, have):
    # set the mail context
    msg = MIMEText(mail_text)

    # set the mail info
    if have == 0:
        msg['Subject'] = "别看了，无"
    else:
        msg['Subject'] = "有了有了！"
    msg['From'] = MAIL_USER
    msg['To'] = mail_to

    # send the mail
    send = smtplib.SMTP_SSL("smtp.163.com", 465)
    send.login(MAIL_USER, MAIL_PWD)
    send.send_message(msg)
    # quit EMail
    send.quit()

def sms(msg):
    app = AppMsgSender(corpid='ww50ff15a2a50fec55',
                       corpsecret='sprY8YyHVVzUJSASK2yr8C-JqyX7s8xKK03skGzZqVM',
                       agentid='1000002')
    app.send_text(content=msg)

def itiscool():
    sms("今天也是正常运行的一天呢")
   
'''
for index in range(0,36):
    if index%2 == 0:
        schedule.every().day.at(daka_time[index]).do(sign_in, users[0])
    else:
        schedule.every().day.at(daka_time[index]).do(sign_in, users[1])

schedule.every().day.at("8:00").do(itiscool)

while True:
    schedule.run_pending()
    time.sleep(1)
'''
checkseats()
itiscool()
