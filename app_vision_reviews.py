# -*- coding: utf-8 -*-
'''  
Athuor: Tristan SHi
Created Date:   2016-09-19
Created Time:   PM4:01 
'''
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import pandas as pd
from dateutil.parser import parse
import time
from random import uniform
from my_packages import ipProxy
import random


def ip_proxy(i):
    hide_df = pd.read_excel('/Users/macbookpro/Desktop/Python/crawler/hide_ass.xlsx')
    ip_pro = hide_df.IP + ':' + hide_df.PORT.map(str)
    proxy = '-proxy-server={ip}'.format(ip=ip_pro[i])
    return proxy


# page源码保存
# page_text_df = pd.DataFrame(columns=['App', 'Page_info', 'Html'])
# IP_index = 0    # 记录IPindex

# 转换日期格式
def date_format(date_str):
    return parse(date_str).strftime('%Y-%m-%d')


# 等待网页加载, 然后点击
def wait_to_click(*args):
    for xpath in list(args):
        wait.until(lambda cd: cd.find_element_by_xpath(xpath))
    time.sleep(0.1)
    xpath = list(args)[0]
    try:
        cd.find_element_by_xpath(xpath).click()
    except:
        ele = cd.find_element_by_xpath(xpath)
        ac.move_to_element(ele).perform()
        ele.click()


# 等待元素加载完毕
def i_am_waiting_for_you(*args):
    for xpath in list(args):
        wait.until(lambda cd: cd.find_element_by_xpath(xpath))


# 页码跳转
def send_page_to_you(shit, xpath):
    i_am_waiting_for_you(xpath)
    hole = cd.find_element_by_xpath(xpath)
    hole.clear()
    hole.send_keys(shit)


# 设置ip代理的
def get_options(df, i):
    proxy = '-proxy-server={ip}'.format(ip=df.ix[i, 'IP'])
    options = webdriver.ChromeOptions()
    options.add_argument(proxy)
    return options


def IP_test():
    IP_ = pd.read_csv('/Users/macbookpro/Desktop/Python/ip.txt')

    for i in range(len(IP_)):
        now = time.time()
        options = get_options(IP_, i)
        cd = webdriver.Chrome('/Users/macbookpro/Desktop/Python/crawler/chromedriver 2', chrome_options=options)
        cd.set_page_load_timeout(20)
        try:
            cd.get('https://www.appannie.com/account/login/?_ref=header')
            IP_.set_value(i, 'Response', time.time() - now)
            cd.quit()
        except:
            IP_.set_value(i, 'Response', 99999)
            cd.quit()
    IP_.sort(['Response'])
    IP_.to_csv('/Users/macbookpro/Desktop/Python/ip.txt')
    return IP_


IP_ = IP_test()

# 登录页面
def login(i=0):
    '''
    loging 随机选择i为log的帐号和密码还有ip
    :param i: i>2的话就不用代理
    :return:
    '''
    global cd, wait, ac, name, password, web, IP_index
    # IP_index += 1
    if i == 0:
        cd = webdriver.Chrome('/Users/macbookpro/Desktop/Python/crawler/chromedriver')
    else:
        options = get_options(IP_, IP_index)
        cd = webdriver.Chrome('/Users/macbookpro/Desktop/Python/crawler/chromedriver 2', chrome_options=options)
    # cd = webdriver.Firefox()
    ac = webdriver.common.action_chains.ActionChains(cd)
    wait = WebDriverWait(cd, 50)
    cd.get('https://www.appannie.com/account/login/?_ref=header')
    name = 'name'
    password = 'password'
    # login
    cd.find_element_by_xpath(".//*[@id='email']").send_keys(name)
    cd.find_element_by_xpath(".//*[@id='password']").send_keys(password)
    cd.find_element_by_xpath(".//*[@id='submit']").click()

    # 语言转为英文
    wait_to_click(".//*[@id='container']/div[3]/div/div[1]/ul[3]/li[1]/a")
    web = 'https://www.appannie.com/apps/ios/app/pokemon-go/details/'



# IP_index = 0    # 记录IPindex


# # 断点验证后重下
# def break_point():
#     reviews.page_swich()
#     reviews.begin_page = beg
#     reviews.get_all_pages_reviews()

def read_csv(path):
    df = pd.read_csv(path)
    df = df.drop(df.columns[0], axis=1)
    df = df.drop_duplicates()
    df.index = list(range(len(df)))
    beg = int(len(df) / 200)
    return df, beg


# 获取更新信息的
class Vision:
    def __init__(self):
        self.app_name = 'Pokémon GO'
        self.vision_df = pd.DataFrame(columns=['App', 'Vision', 'Date', 'Contents'])

    def get_each_visions(self):
        cd.get('https://www.appannie.com/apps/ios/app/pokemon-go/details/')
        i_am_waiting_for_you(".//*[@id='app_content']/div[3]/div[2]/a/span")  # 等待JS执行完毕
        page_text_df.loc[len(page_text_df)] = [self.app_name, 'visions', cd.page_source]
        tree = etree.HTML(cd.page_source)
        vision_title = tree.xpath(".//*[@id='app_content']/div[3]/div/h5/text()")  # vision+date
        f = lambda x: x.replace(')', '').split('(')
        vision_title = list(map(f, vision_title))

        for i, ele in enumerate(vision_title):  # 转换日期为mysql接受的格式
            vision_title[i][1] = date_format(ele[1])

        for i in range(len(vision_title)):
            text = ''.join(tree.xpath(".//*[@id='app_content']/div[3]/div[1]/div[%s]/p/text()" % str(i + 1)))
            vision_title[i].append(text)
            vision_title[i].insert(0, self.app_name)
            self.vision_df.loc[i] = vision_title[i]
        time.sleep(uniform(0.9, 2.0))


# 获取review信息的
class review:
    def __init__(self, begin):
        '''
        :param begin: 开始下载的页码
        '''
        self.app_name = 'Pokémon GO'
        self.reviews_df = pd.DataFrame(columns=['App', 'Country', 'Date', 'Rating', 'Review_content', 'Reviewer_name',
                                                'Reviewer_title', 'Vision'])
        self.page_num = None
        self.ratings = None
        self.begin_page = begin  # 开始爬的页数
        self.current_page = None  # 正在爬取的页码

    def page_swich(self):
        '''
        cd
        :return: 切换页面到reviews, 选择到所有时间, 选择每页显示200项
        '''

        cd.find_element_by_link_text("Reviews").click()  # 切换到review界面
        wait.until(lambda cd: cd.find_element_by_link_text("Date Range"))
        wait.until(lambda cd: cd.find_element_by_link_text("Rating"))
        wait_to_click(".//*[@id='aa-app']/div/div/div[1]/div[1]/div[6]/a[1]/span[1]",
                      ".//*[@id='aa-app']/div/div/div[1]/div[1]/div[6]/a[1]/span[2]")
        wait_to_click("html/body/div[4]/div[1]/a[1]")
        # "html/body/div[4]/div[1]/a[1]",
        #           ".//*[@id='overlay']")            # 选择到所有时间
        time.sleep(uniform(1.0, 2.0))

        # 切换到reviews从高到底排列
        wait_to_click \
                (
                ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/p")
        time.sleep(uniform(1.0, 2.0))

        # 选择每页显示200项
        wait.until(lambda cd: cd.find_element_by_link_text("Rating"))
        wait_to_click(".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[1]/select",
                      ".//*[@id='aa-app']/div/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]")
        wait_to_click(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[1]/select/option[4]")
        time.sleep(uniform(1.0, 2.0))
        wait.until(lambda cd: len(etree.HTML(cd.page_source).xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/span/strong/text()")) != 10
                   )

        # 切换到断点页面
        self.next_reviews_page(beg)

    # 获取总共的页码, 还有ratings的信息的
    def get_basic_info(self):
        '''
        :return: total page_num, ratings num for each level
        '''
        self.page_swich()
        tree = etree.HTML(cd.page_source)
        vals = tree.xpath(".//*[@id='aa-app']/div/div/div[2]/div[1]/div[3]/div[2]/div/table/tbody/tr/td[3]/text()")
        ratings = list(map(lambda x: int(x.replace(',', '')), vals))
        for i in range(1, len(ratings)):
            ratings[i] += ratings[i - 1]
        self.ratings = ratings  # 返回一个star数的list, 从5星到1星排序

        page_num = int(tree.xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[2]/span/text()")[
                           0].replace('/', '').strip())
        self.page_num = page_num

    # 切换ip用,但太慢, 先不使用
    def swich_ip(self, num):
        cd.quit()
        while True:
            try:
                login(i=random.randint(0, 3))
            except:
                continue
        cd.get(web)
        self.page_swich()

    # 获取每一页200个的reviews的信息
    def get_each_page_reviews(self, page_num):
        tree = etree.HTML(cd.page_source)
        # 得到reivewer name, title, contents的一个list
        # page_text_df.loc[len(page_text_df)] = [self.app_name, 'reviews_page %s'%str(page_num), cd.page_source]
        reviewers_name = tree.xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/span/strong/text()")
        reviews_title = tree.xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/strong/text()")
        reviews_content = tree.xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/text()")
        reviews_date = tree.xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[3]/div[2]/div/span/text()")
        reviews_date = list(map(lambda x: date_format(x), reviews_date))
        reviews_country = tree.xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[4]/div[2]/div/span/text()")
        reviews_country = list(map(lambda x: x.strip(), reviews_country))
        reviews_vision = tree.xpath(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[5]/div[2]/div/span/text()")
        for i in range(len(reviewers_name)):
            for j, val in enumerate(self.ratings):
                if len(self.reviews_df) >= val:
                    continue
                else:
                    break
            rate = 5 - j

            self.reviews_df.loc[len(self.reviews_df)] = [self.app_name, reviews_country[i], reviews_date[i], rate,
                                                         reviews_content[i],
                                                         reviewers_name[i], reviews_title[i], reviews_vision[i]]

    # 切换页码
    def next_reviews_page(self, num):
        time.sleep(uniform(0.7, 1.5))
        send_page_to_you('%s\n' % str(num),
                         ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[2]/input")
        time.sleep(uniform(0.7, 1.5))
        i_am_waiting_for_you(
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/p/span",
            ".//*[@id='aa-app']/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div[3]/div/div/div[2]/button[3]",
            ".//*[@id='aa-app']/div/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]")
        time.sleep(uniform(12.012, 20.023))

    # 存储爬取的信息
    def save_reviews_info(self, name):
        # self.reviews_df.columns = ['App', 'Rating', "Reviewer_name", 'Reviewer_title', 'Review_content', 'Date', 'Country', 'Vision']
        self.reviews_df.to_csv('/Users/macbookpro/Desktop/Python/crawler/Task2/' + name + '.csv', encoding='utf-8')
        self.reviews_df.to_excel('/Users/macbookpro/Desktop/Python/crawler/Task2/' + name + '.xlsx', encoding='utf-8')

    # 获取所有页码的reviews信息
    def get_all_pages_reviews(self):
        # circle = 0
        # while circle < 3:
        try:
            for i in range(self.begin_page + 1, self.page_num + 1):
                global beg
                beg = i
                self.get_each_page_reviews(i - 1)
                self.current_page = i  # 记录正在爬的页面
                time.sleep(uniform(0.7, 1.5))
                # 用于翻页
                self.next_reviews_page(num=i)

                # if i % 100 == 0:
                #     self.swich_ip(i)
                #     continue  # swich ip proxy and account

                if i % 100 == 0:
                    print(i)
                    cd.quit()
                    login(5)
                    cd.get('https://www.appannie.com')
                    cd.get('https://www.appannie.com/apps/ios/app/pokemon-go/details/')
                    self.page_swich()
                    time.sleep(uniform(300, 500))

            self.save_reviews_info('all_reviews')

        except:
            self.save_reviews_info('part_reviews')
            global beg
            beg = i  # 记录已经下载到的页码
            print(time.time())
            raise ConnectionError
            # cd.quit()
            # print(circle, time.time())
            # time.sleep(uniform(1000, 2000))
            # login(5)
            # cd.get('https://www.appannie.com/apps/ios/app/pokemon-go/details/')
            # self.page_swich()
            # circle += 1


def main():
    df, beg = read_csv(path)
    login(i=2)
    vision = Vision()
    vision.get_each_visions()

    reviews = review(beg)
    reviews.reviews_df = df
    reviews.get_basic_info()
    reviews.get_all_pages_reviews()


if __name__ == '__main__':
    main()

