# -*- coding: utf-8 -*
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
        if flag and (rsp.ret_code == 0):
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

    time.sleep(1000)
    #browser.quit()
    return 1;

def checksetas():
    tb = pd.read_html('../Downloads/教育部考试中心GRE考试报名网.html')
    t1 = tb[1]
    print(t1)
    
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
    rsp = captcha_pred(src,api)
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
    print(string)
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

def sub_info(browser, user):
    browser.get('http://bcfl.sdufe.edu.cn/student/handle_ext.html')
    province = Select(browser.find_element_by_id('province_id'))
    province.select_by_visible_text(user.province)
    time.sleep(1)
    city = Select(browser.find_element_by_id('city_id'))
    city.select_by_visible_text(user.city)
    auth_img=browser.find_element_by_class_name('auth_code_img')
    print("Found Image with that auth_code_img!" )
    captcha=browser.find_element_by_id('verify')
    print("Found <%s> element with that verify!" % (captcha.tag_name))
    sub_bt=browser.find_element_by_id('student_btn')
    print("Found <%s> element with that sub_btn!" % (sub_bt.tag_name))
    action = ActionChains(browser)
    action.context_click(auth_img).perform() #右键点击该元素

    #选中右键菜单中第3个选项
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(5)
    os.system('xclip -selection clipboard -t image/png -o > ./img.png')
    rsp=captcha_pred()
    captcha.send_keys(rsp.pred_rsp.value)
    sub_bt.click()
    
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.alert_is_present())
        alert = browser.switch_to.alert
        if alert.text == "请输入有效验证码":
            logging.info("Captcha for user <{0}> is wrong, now try again.".format(user.uid))
            alert.accept()
            browser.quit()
            if rsp.ret_code == 0:
                api = FateadmApi(app_id, app_key, pd_id, pd_key)
                api.Justice(rsp.request_id)
        return 0;
    except TimeoutException:
        return 1;
    return 1;

def mail(mail_text, mail_to):
    # set the mail context
    msg = MIMEText(mail_text)

    # set the mail info
    msg['Subject'] = "今日打卡状态"
    msg['From'] = MAIL_USER
    msg['To'] = mail_to

    # send the mail
    send = smtplib.SMTP_SSL("smtp.163.com", 465)
    send.login(MAIL_USER, MAIL_PWD)
    send.send_message(msg)
    # quit EMail
    send.quit()

def daily():
    for user in users:
        logging.info("Get user <{0}> form user list.".format(user.uid))
        mark=0
        while(mark==0):
            mark = sign_in(user)
        msg = user.uid + ": 打卡成功"
        mail(msg, user.email)
        logging.info("Emailing to User {0} for notification".format(user.uid))
    logging.info("Emailing is finished")

daily()
schedule.every().day.at(daka_time).do(daily)
while True:
    schedule.run_pending()
    time.sleep(1)
