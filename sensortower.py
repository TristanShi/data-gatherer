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
from selenium.webdriver.chrome.options import Options
from random import uniform, randint
import pandas as pd
from datetime import datetime
import functools
import codecs


db = mysql.connector.connect(user='', password='',
                             host='127.0.0.1',
                             database='sensortower')
mycursor = db.cursor()
df = pd.read_csv('.../us_app_id_list.txt')



def now_time(fn):

    @functools.wraps(fn)
    def wrapper(*args):
        fn(*args)
        print(args[1:], datetime.now().strftime("%H:%M:%S"))

    return wrapper

def sleep(a,b):
    time.sleep(uniform(a, b))
    return

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
                driver = Driver('https://sensortower.com/ios/us/facebook-inc/app/%s' % shit)
                driver.login()
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


'''
username: [xpath_path, username]
passname: [xpath_path, password]
'''
class Driver(object):
    def __init__(self, landing_page='', username=[], password=[]):
        self.land = landing_page        #登录页面
        self.username = username
        self.password = password


    @staticmethod
    def set_ops():
        from user_agent import generate_user_agent
        opts = Options()
        ua = generate_user_agent()
        opts.add_argument("user-agent=%s" % ua)
        return opts

    def login(self, url=None):
        global cd, wait
        cd = webdriver.Chrome('C:/Users/tristanshi/Desktop/chromedriver.exe', chrome_options=Driver.set_ops())
        wait = WebDriverWait(cd, 50)
        cd.get(url) if url is not None else cd.get(self.land)
        click(".//*[@id='register-modal']/a")       # 根据情况加的,主要作用关掉登录窗口
        sleep(0.2, 0.9)

        if len(self.username) == 0 or len(self.password) == 0:
            return cd,wait
        else:
            # login
            pass
            return cd,wait

def login(url):
    driver = Driver(landing_page=url)
    driver.login()
    return 'Come On!!'


class sensortower():
    def __init__(self, beg=50000, end= 100000, path=''):
        self.begin = beg
        self.end = end
        self.num = 0
        self.path = path

    # 页码跳转
    def send_app_to_you(self, num, shit):

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
                    # driver = Driver('https://sensortower.com/ios/us/facebook-inc/app/%s' % shit)
                    # driver.login()
                    click(".//*[@id='register-modal']/a")
                    if check_exist(".//*[@id='primary-app-search-field']"):
                        pass
                    else:
                        sleep(25.0, 30.03)
                        cd.refresh()
                        click(".//*[@id='register-modal']/a")

        if num > randint(7, 11):
            try:
                cd.get('https://sensortower.com/ios/us/facebook-inc/app/%s' % shit)
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

    @now_time
    def _get_info(self,  index, app_id):
        tree = etree.HTML(cd.page_source)
        month = ''.join(tree.xpath(".//*[@id='app-revenue-downloads']/div[1]/a[1]/span[2]/span/text()"))
        download = ''.join(tree.xpath(".//*[@id='app-revenue-downloads']/div[1]/a[1]/span[1]/text()"))
        revenue = ''.join(tree.xpath(".//*[@id='app-revenue-downloads']/div[1]/a[2]/span[1]/text()"))

        pa = [index + 1, app_id, month, download, revenue]
        mycursor.execute("""INSERT INTO app VALUES (%s, %s, %s, %s, %s)""", params=pa)
        # html = str(cd.page_source.encode('utf-8'))
        with codecs.open(self.path + app_id+'.txt', 'w', 'utf-8') as f:
            f.write(cd.page_source)
        db.commit()
        # print(index + 1, app_id, now_time())

        return 1



    def get_all_pages_info(self):
        mycursor.execute("""SELECT app_id FROM app""")
        app_id_list = list(map(lambda x: x[0].strip(','), mycursor.fetchall()))
        for i in range(self.begin, self.end):
            # check是否已经存在
            app_id = str(df.ix[i, 'app_id'])
            if app_id in app_id_list:
                continue
            click(".//*[@id='register-modal']/a")
            try:
                i_am_waiting_for_you(".//*[@id='all-time-reviews']/div[1]/div/div[2]/div/table/tbody")
            except:
                sleep(15.43, 22.43)
                cd.refresh()
                click(".//*[@id='register-modal']/a")
                if check_exist(".//*[@id='primary-app-search-field']"):
                    pass
                else:
                    self.send_app_to_you(self.num, app_id)
                    continue

            self._get_info(i, app_id)

            if i % 100 == 0:
                cd.quit()
                sleep(7.2, 8.4)
                login('https://sensortower.com/ios/us/facebook-inc/app/%s'%app_id)
                # driver = Driver(landing_page='https://sensortower.com/ios/us/facebook-inc/app/%s'%app_id)
                # driver.login()
            else:
                self.num += 1
                send_app_to_you(self.num, app_id)
                if self.num > randint(17,20):
                    self.num = 0


def main():
    st = sensortower(beg=0, path='.../page_source/')
    login(url='https://sensortower.com/ios/us/facebook-inc/app/%s'%str(df.ix[st.begin, 'app_id']))
    st.get_all_pages_info()

if __name__ == '__main__':
    main()











