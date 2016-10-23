# -*- coding: utf-8 -*-

'''  
@ Athuor: Tristan SHi
@ Created Date:   12/10/2016
@ Created Time:   4:53 PM
@ Contact: fineshi@foxmail.com
'''

import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import time
from user_agent import generate_user_agent
from selenium.webdriver.chrome.options import Options
from random import uniform, randint
from dateutil.parser import parse
from datetime import timedelta
import datetime

# 连接数据库
db = mysql.connector.connect(user='username', password='password',
                             host='127.0.0.1',
                             database='app_annie',
                             charset='utf8mb4')     # 需要插入表情或其他特殊字符数据
mycursor = db.cursor()


# 转换日期格式
def time_format(time_str):
    return parse(time_str).strftime('%Y-%m-%d %H:%M:%S')


def date_format(date_str):
    return parse(date_str).strftime('%Y-%m-%d')


# 计算日期
def date_cal(date, interval):
    date = parse(date) + timedelta(interval)
    return date.strftime('%Y-%m-%d')


# 设置user-agent
def set_ops():
    opts = Options()
    ua = generate_user_agent()
    opts.add_argument("user-agent=%s" % ua)
    return opts


# 等待元素加载完毕
def i_am_waiting_for_you(*args):
    for xpath in list(args):
        wait.until(lambda cd: cd.find_element_by_xpath(xpath))


def sleep(a, b):
    time.sleep(uniform(a, b))
    return


def wait_to_click(*args):
    i_am_waiting_for_you(*args)
    sleep(0.1, 0.2)
    xpath = list(args)[0]
    cd.find_element_by_xpath(xpath).click()
    sleep(0.2, 0.3)


def click(xpath):
    try:
        cd.find_element_by_xpath(xpath).click()
    except:
        pass


def check_exist(xpath):
    try:
        cd.find_element_by_xpath(xpath)
        sleep(0.2, 0.3)  # 如果正确， 停顿一下
        return True
    except:
        return False


def login():
    '''
    loging 随机选择i为log的帐号和密码还有ip
    :param i: i>2的话就不用代理
    :return:
    '''
    global cd, wait, ac, name, password, web, IP_index
    # IP_index += 1
    cd = webdriver.Chrome('path of chromedriver', chrome_options=set_ops())
    # cd = webdriver.Firefox()
    ac = webdriver.common.action_chains.ActionChains(cd)
    wait = WebDriverWait(cd, 50)
    cd.get(
        'https://www.appannie.com/apps/ios/top-chart/united-states/overall/?device=iphone&date=2016-10-13&feed=All&metrics=&rank_sorting_type=&desc=t&order_by=sort_order&page_number=0&page_size=100')
    name = 'name'
    password = 'password'
    # login
    cd.find_element_by_xpath(".//*[@id='email']").send_keys(name[i])
    cd.find_element_by_xpath(".//*[@id='password']").send_keys(password[i])
    cd.find_element_by_xpath(".//*[@id='submit']").click()

    # 语言转为英文
    wait_to_click(".//*[@id='container']/div[3]/div/div[1]/ul[3]/li[1]/a")
    web = 'https://www.appannie.com/apps/ios/app/pokemon-go/details/'
    sleep(2.0, 3.2)

    # 切换到显示500个每页
    wait_to_click(".//*[@id='aa-app']/div/div/div[1]/div[2]/div[2]/div/div[3]/select")
    sleep(0.2, 0.6)
    wait_to_click(".//*[@id='aa-app']/div/div/div[1]/div[2]/div[2]/div/div[3]/select/option[2]")
    sleep(1.0, 1.2)


# 提取每页的数据
def get_page_text(tree, parent_cat=None):
    def check_charge(s):
        if s is '':
            return 0
        if '$' in s:
            s = 1
            return s

    def check_change(s):
        if s is None:
            return None
        s = s.replace('▲', '+')
        s = s.replace('▼', '-')
        return s

    # get change text and developer list
    def change_text(path):
        nodes = tree.xpath(path)
        return [check_change(node.text) for node in nodes]

    # get charge text list
    def charge_text(path):
        nodes = tree.xpath(path)
        return [check_charge(''.join(node.xpath(".//div[3]/span/text()"))) for node in nodes]

    url = cd.current_url
    utctime = ''.join(tree.xpath(".//*[@id='aa-app']/div/div/div[1]/div[2]/div[1]/h3/span/span/span/text()")).strip()
    date = date_format(utctime)
    time = time_format(utctime)

    category = ''.join(tree.xpath(".//*[@id='aa-app']/div/div/div[1]/div[1]/div/div[3]/a[1]/text()"))
    classes = ['free', 'paid', 'grossing']
    for col in range(2, 5):
        name = change_text(
            ".//*[@id='aa-app']/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr/td[{col}]/div/div[1]/div/a[1]/span"
                .format(col=col))
        cat = change_text(
            ".//*[@id='aa-app']/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr/td[{col}]/div/div[1]/div/a[2]/span"
                .format(col=col))
        href = tree.xpath(
            ".//*[@id='aa-app']/div/div/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr/td[{col}]/div/div[1]/div/a[1]/@href"
                .format(col=col))
        change = change_text(
            ".//*[@id='aa-app']/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr/td[{col}]/div/div[2]/div/span"
                .format(col=col))
        charge = charge_text(
            ".//*[@id='aa-app']/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr/td[{col}]/div"
                .format(col=col))

        for i in range(0, len(name)):
            rank = i + 1
            params = [classes[col - 2], rank, str(change[i]), date, time, parent_cat, category, str(name[i]),
                      str(href[i]),
                      str(cat[i]), str(charge[i]), url]

            mycursor.execute(
                """INSERT INTO rank (class, rank, rank_change, date_, time_, parent_cat, category , app_name, app_href, developer, in_app_charge, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                params=params)
            db.commit()

    # 保存页面源代码
    mycursor.execute("""INSERT INTO page VALUES (%s, %s, %s)""", params=[date, category, None])
    db.commit()

    return date


# 获取日期的点击位置
def get_date_location(date):
    day = int(date[-2:])
    weekday = parse(date[:-2] + '01').weekday()

    # 星期天对应的是num = 6， 但在第一格
    if weekday == 6:
        loc_col = 1
    else:
        loc_col = weekday + 2

    interval = day - 1

    # loc_tr和loc_td分别对应竖排和横排位置
    loc_td = interval % 7 + loc_col
    if loc_td > 7:
        loc_td = loc_td - 7
        loc_tr = int(interval / 7) + 2
    else:
        loc_tr = int(interval / 7) + 1
    return loc_tr, loc_td


# 获取每个category下的子日期数据
def date_change(date):
    page_date = date_format(cd.find_element_by_xpath(".//*[@id='aa-app']/div/div/div[1]/div[1]/div/div[5]/a[1]").text)
    if page_date == date:
        return date

    page_month = parse(page_date).month
    month = parse(date).month
    wait_to_click("html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[5]/a[1]")
    sleep(0.2, 0.3)
    if page_month != month:
        cd.find_element_by_css_selector(".ui-datepicker-month").click()
        sleep(0.1, 0.2)
        wait_to_click('//*[@class="aa-popup"]/div/div/div/div/div/select[1]/option[{s}]'.format(s=month))

    loc_tr, loc_td = get_date_location(date)

    # 用绝对路径会好些，因为这个网站的定位id随机生成的
    wait_to_click('html/body/div/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{tr}]/td[{td}]/a'
                  ''.format(tr=loc_tr, td=loc_td))
    sleep(2.4, 3.8)
    return date


def get_category_pages(category, parent_cat=None):
    # 网站数据迟一天出来， 所以默认减一天
    date = date_cal(datetime.datetime.now().strftime('%Y-%m-%d'), -1)
    # 如果已经爬取过， 跳过
    mycursor.execute("""SELECT date_ FROM page WHERE category=%s""", params=[category])
    _date = list(map(lambda x: x[0].strftime('%Y-%m-%d'), mycursor.fetchall()))

    # 如果数据已经存在的话就跳过, 直到不存在的那天
    while date != '2016-07-31':
        if date in _date:
            date = date_cal(date, -1)
            continue
        else:
            # date = date_cal(date, 1)
            break

    if date == '2016-07-31':
        return
    else:
        date = date_change(date)

    while date != '2016-07-31':
        i_am_waiting_for_you(
            ".//*[@id='aa-app']/div/div/div/div[2]/div[2]/div/div[2]/div/table/thead/tr/th[2]/div/span")
        sleep(0.3, 0.8)
        date = get_page_text(etree.HTML(cd.page_source), parent_cat)
        print('         ', date)
        # 日期改变
        if date == '2016-08-01':
            break
        date_change(date_cal(date, -1))


# 获取26个大类的pages 信息
def get_all_pages(beg=0, end=0):
    # get_category_pages('Overall')
    # 点击category获取category的类别信息

    wait_to_click("html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[3]/a[1]")
    sleep(0.2, 0.5)
    # 获取category的list
    cats = list(map(lambda x: x.text, etree.HTML(cd.page_source).xpath(".//*[@class='aa-popup']/div/ul/li/a/span")))
    end = len(cats)
    # now_date = date_cal(datetime.datetime.now().strftime('%Y-%m-%d'), -1)
    wait_to_click("html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[3]/a[1]")

    for i in range(beg, end):
        wait_to_click("html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[3]/a[1]")
        sleep(0.3, 0.5)
        wait_to_click('//*[@id="aa-app"]/div/div/div/div[1]/ul/li[{cat}]/a'.format(cat=i))
        print(cats[i - 1])
        i_am_waiting_for_you('//*[@id="aa-app"]/div/div/div[1]/div[2]/div[2]/div/div[3]/select')
        # date_change(now_date)
        sleep(0.5, 0.8)
        get_category_pages(category=cats[i - 1])
        sleep(4.0, 5.3)


# 获取小类的pages信息
def get_subcat_pages(beg=0, end=3):
    parent_cats_path = ['//*[@id="aa-app"]/div/div/div[2]/div[1]/ul[1]/li[9]/a[2]',
                        '//*[@id="aa-app"]/div/div/div[2]/div[1]/ul[1]/li[11]/a[2]',
                        '//*[@id="aa-app"]/div/div/div[2]/div[1]/ul[1]/li[13]/a[2]']  # game, kids, magazines and newspaper
    parent_cats = ['Game', 'Kids', 'Magazines and Newspapers']
    for i in range(beg, end):
        wait_to_click("html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[3]/a[1]")
        wait_to_click(parent_cats_path[i])
        cats = list(map(lambda x: x.text,
                        etree.HTML(cd.page_source).xpath('//*[@id="aa-app"]/div/div/div[2]/div[1]/ul[2]/li/a/span')))
        wait_to_click("html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[3]/a[1]")
        print(parent_cats[i])

        for j in range(1, len(cats) + 1):
            wait_to_click("html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[3]/a[1]")
            sleep(0.3, 0.5)
            wait_to_click(parent_cats_path[i])
            sleep(0.3, 0.5)
            wait_to_click('//*[@id="aa-app"]/div/div/div[2]/div[1]/ul[2]/li[{j}]/a/span'.format(j=j))
            print('     ', cats[j - 1])
            i_am_waiting_for_you('//*[@id="aa-app"]/div/div/div[1]/div[2]/div[2]/div/div[3]/select')
            get_category_pages(category=cats[j - 1], parent_cat=parent_cats[i])
            sleep(1.0, 2.3)


def main():
    login()
    get_all_pages()
    get_subcat_pages()


if __name__ == '__main__':
    main()







