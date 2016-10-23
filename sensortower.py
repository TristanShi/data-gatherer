# -*- coding: utf-8 -*-

'''
@ Athuor: Tristan SHi
@ Created Date:   12/10/2016
@ Created Time:   10:55 AM
@ Contact: fineshi@foxmail.com
'''

import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import time
from user_agent import generate_user_agent
from selenium.webdriver.chrome.options import Options
from random import uniform, randint
import pandas as pd



db = mysql.connector.connect(user='', password='',
                             host='127.0.0.1',
                             database='sensortower',
                             charset='utf8mb4')
mycursor = db.cursor()
df = pd.read_csv('/Users/macbookpro/Dropbox/scraping/Task 5 SenseTower/us_app_id_list.txt')


def sleep(a,b):
    time.sleep(uniform(a, b))
    return

# 设置user-agent
def set_ops():
    opts = Options()
    ua = generate_user_agent()
    opts.add_argument("user-agent=%s"%ua)
    return opts

def login(url=None):
    global cd, wait, ac, name, password, web, IP_index
    cd = webdriver.Chrome('/Users/macbookpro/Desktop/Python/crawler/chromedriver', chrome_options=set_ops())
    wait = WebDriverWait(cd, 50)
    if url is not None:
        cd.get(url)
    cd.get('https://sensortower.com/ios/us/facebook-inc/app/facebook/284882215/')
    click(".//*[@id='register-modal']/a")
    sleep(0.2, 0.9)

# 等待元素加载完毕
def i_am_waiting_for_you(*args):
    for xpath in list(args):
        wait.until(lambda cd: cd.find_element_by_xpath(xpath))

def wait_to_click(*args):
    i_am_waiting_for_you(*args)
    sleep(0.1, 0.2)
    xpath = list(args)[0]
    cd.find_element_by_xpath(xpath).click()

def click(xpath):
    try:
        cd.find_element_by_xpath(xpath).click()
    except:
        pass

def check_exist(xpath):
    try:
        cd.find_element_by_xpath(xpath)
        sleep(0.2, 0.3)     # 如果正确， 停顿一下
        return True
    except:
        return False


# 页码跳转
def send_app_to_you(num, shit):
    def ex_d():
        sleep(7.0, 9.67)
        cd.get('https://sensortower.com/ios/us/facebook-inc/app/%s' % shit)
        if check_exist(".//*[@id='primary-app-search-field']"):
            pass
        else:
            sleep(10.0, 15.23)
            cd.refresh()
            click(".//*[@id='register-modal']/a")
            if check_exist(".//*[@id='primary-app-search-field']"):
                pass
            else:
                cd.quit()
                sleep(15.0, 20.23)
                login('https://sensortower.com/ios/us/facebook-inc/app/%s' % shit)
                click(".//*[@id='register-modal']/a")
                if check_exist(".//*[@id='primary-app-search-field']"):
                    pass
                else:
                    sleep(25.0, 30.03)
                    cd.refresh()
                    click(".//*[@id='register-modal']/a")

    if num > randint(7, 11):
        try:
            cd.get('https://sensortower.com/ios/us/facebook-inc/app/%s'%shit)
            click(".//*[@id='register-modal']/a")
            sleep(2.0, 3.5)
            cd.find_element_by_xpath(".//*[@id='app-revenue-downloads']/div[1]/a[1]/span[2]/span/text()")
        except:
            ex_d()

    else:
        i_am_waiting_for_you(".//*[@id='all-time-reviews']/div[1]/div/div[2]/div/table/tbody")
        real_shit = shit + '\n'
        hole = cd.find_element_by_xpath(".//*[@id='primary-app-search-field']")
        hole.clear()
        hole.send_keys(real_shit)
        try:
            wait_to_click(".//*[@id='ui-id-1']/li/a/div")
            click(".//*[@id='register-modal']/a")
        except:
            ex_d()

    click(".//*[@id='register-modal']/a")
    sleep(1.17, 3.01)
    return


class sensortower():

    def __init__(self, beg=1, end= len(df)):
        self.begin = beg
        self.end = end
        self.num = 0

    def get_all_pages_info(self):
        mycursor.execute("""SELECT app_id FROM app""")
        app_id_list = list(map(lambda x: x[0].strip(','), mycursor.fetchall()))
        for i in range(self.begin, self.end):
            # check是否已经存在
            click(".//*[@id='register-modal']/a")
            app_id = str(df.ix[i, 'app_id'])
            if app_id in app_id_list:
                continue

            try:
                i_am_waiting_for_you(".//*[@id='all-time-reviews']/div[1]/div/div[2]/div/table/tbody")
            except:
                sleep(7.43, 17.43)
                cd.refresh()
                click(".//*[@id='register-modal']/a")
                if check_exist(".//*[@id='primary-app-search-field']"):
                    pass
                else:
                    continue

            tree = etree.HTML(cd.page_source)
            month = ''.join(tree.xpath(".//*[@id='app-revenue-downloads']/div[1]/a[1]/span[2]/span/text()"))
            download = ''.join(tree.xpath(".//*[@id='app-revenue-downloads']/div[1]/a[1]/span[1]/text()"))
            revenue = ''.join(tree.xpath(".//*[@id='app-revenue-downloads']/div[1]/a[2]/span[1]/text()"))

            pa = [app_id, month, download, revenue]
            mycursor.execute("""INSERT INTO app VALUES (%s, %s, %s, %s)""", params=pa)
            html = str(cd.page_source.encode('utf-8'))
            mycursor.execute("""INSERT INTO page VALUES (%s, %s)""", params=[app_id, html])
            db.commit()

            if i % 100 == 0:
                cd.quit()
                sleep(7.2, 8.4)
                login('https://sensortower.com/ios/us/facebook-inc/app/%s'%app_id)
            else:
                self.num += 1
                send_app_to_you(self.num, app_id)
                if self.num > randint(17,20):
                    self.num = 0


def main():
    login()
    st = sensortower()
    st.get_all_pages_info()

if __name__ == '__main__':
    main()











