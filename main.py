# -*- coding: utf-8 -*
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fateadm_api import *
from info import *
from email.mime.text import MIMEText
import schedule
import smtplib
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
    browser = webdriver.Chrome()
    browser.get('https://gre.neea.cn/')
    time.sleep(3)
    logging.info("Successfully get chrome driver.")
    neeaId=browser.find_element_by_id('neeaId')
    print("Found <%s> element with that number!" % (neeaId.tag_name))
    password=browser.find_element_by_id('password')
    print("Found <%s> element with that card!" % (password.tag_name))
    code=browser.find_element_by_id('checkImageCode')
    print("Found <%s> element with that verify!" % (code.tag_name))
    #sign_bt=browser.find_element(By.XPATH,'//button[text()="Some Text"]')
    #print("Found <%s> element with that sub_btn!" % (sign_bt.tag_name))
    action = ActionChains(browser)
    action.context_click(code).perform()
    chkImg=browser.find_element_by_id('chkImg')
    print("Found <%s> element with that auth_code_img!" % (chkImg.tag_name))

    number.send_keys(user.uid)
    password.send_keys(user.pwd)
    rsp=captcha_pred(chkImg.src)
    code.send_keys(rsp.pred_rsp.value)
    #press enter
    send_keys(Keys.ENTER)

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
        elif alert.text == "工号或密码错误，请重新输入！":
            logging.DEBUG("Password for user <{0}> is wrong, now try again.".format(user.uid))
        return 0;
    except TimeoutException:
        success_sub=0
        while success_sub==0:
            success_sub = sub_info(browser, user)

    browser.quit()
    return 1;

def captcha_pred(url):
    #识别类型， 具体类型可以查看官方网站的价格页选择具体的类型
    pred_type = "20400"
    api = FateadmApi(app_id, app_key, pd_id, pd_key)
    # 查询余额
    balance = api.QueryBalcExtend()   # 直接返余额
    # 如果不是通过文件识别，则调用Predict接口：
    # result             = api.PredictExtend(pred_type,data)       # 直接返回识别结果
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
        flag=0
        while(flag==0):
            flag = sign_in(user)
        msg = user.uid + ": 打卡成功"
        mail(msg, user.email)
        logging.info("Emailing to User {0} for notification".format(user.uid))
    logging.info("Emailing is finished")

daily()
schedule.every().day.at(daka_time).do(daily)
while True:
    schedule.run_pending()
    time.sleep(1)
