# -*- coding: utf-8 -*-
'''
Athuor: Tristan SHi
Current Date:   2016-08-18
Current Time:   11:17 AM
'''

'''
时间为美国时间
返回0: 代表获取失败
返回1: 代表获取成功
返回2: 代表已经存在数据库中'''

import facebook
import json
import requests
import time
import dateutil.parser
from pytz import timezone
import pandas as pd
from dateutil.parser import parse
import functools
import pymongo
import sys

client = pymongo.MongoClient()
db = client.facebook


# 时间格式转换,方便后期转入结构化数据库
def date_format(_date):
    try:
        result = parse(_date).strftime("%Y-%m-%d")
        return result
    except:
        return _date


# 时区转换, 转为美国时间
def change_timezone(time_):
    try:
        central = timezone("US/Central")
        utc_time = dateutil.parser.parse(time_)
        US_time = utc_time.astimezone(central)
        return US_time.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return time_


# 计算程序时间的装饰器
def count_time(fn):
    now = time.time()

    @functools.wraps(fn)
    def wrapper(*args):
        print('%s Ready go ' % str(args[1]))
        fn(*args)
        print('%s Running time: ' % str(args[1]), round(time.time() - now, 7), 's')
        return 1

    return wrapper


# 用于捕获异常并放入数据库
def catch_exception(value={}):
    def decorator(fn):

        @functools.wraps(fn)
        def wrapper(*args):
            try:
                fn(*args)
                return 1
            except:
                exception = str(sys.exc_info()[1])
                value['exception'], value[fn.__name__] = exception, args[1]
                db.skipped_table.insert_one(value)
                return 0

        return wrapper

    return decorator


class fbSDK:
    def __init__(self, beg=0, path='C:/Users/tristanshi/Dropbox/program/1000actor.xlsx'):
        self._access_token = ""
        self._graph = facebook.GraphAPI(self._access_token, timeout=20)
        self.df = pd.read_excel(path)
        self.df.index = list(range(len(self.df)))
        self.df['down_record'] = 0
        self.beg = beg
        self.post_id_list = db.post.distinct('id')  # 用于检查数据库中是否已经存在 post
        self.page_id_list = db.page.distinct('id')  # 用于检查数据库中是否已经存在 page

    # 抓取page信息放入MongoDB数据库
    @catch_exception(value={'other_info': 'get page_info'})
    def page_info(self, page_id):
        profile = self._graph.get_object(
            '%s?fields=about,affiliation,app_links,band_interests,band_members,best_page,bio,birthday,booking_agent,can_post,category,checkins,cover,current_location,description,description_html,display_subtext,displayed_message_response_time,emails,engagement,fan_count,featured_video,founded,general_info,general_manager,genre,global_brand_page_name,has_added_app,hometown,impressum,influences,is_always_open,is_community_page,is_permanently_closed,is_published,is_unclaimed,is_verified,leadgen_tos_accepted,link,location,mission,name,name_with_location_descriptor,id,parking,personal_info,personal_interests,phone,place_type,press_contact,record_label,release_date,single_line_address,start_info,talking_about_count,username,verification_status,voip_info,website,were_here_count' % page_id)

        # 判断page_id是否已经存在在数据库
        if page_id in self.page_id_list:
            return 2

        if 'release_date' in profile.keys():
            profile['release_date'] = date_format(profile['release_date'])

        if 'birthday' in profile.keys():
            profile['birthday'] = date_format(profile['birthday'])

        db.page.insert_one(profile)
        return 1

    # Get posts_info and insert it to mongodb
    @catch_exception(value={'other_info': 'get posts_info'})
    def posts_info(self, post_from_id):
        posts = self._graph.get_object(
            '%s/posts?fields=application,admin_creator,caption,created_time,description,from,id,icon,is_expired,is_hidden,is_instagram_eligible,is_published,is_popular,link,message,message_tags,name,object_id,parent_id,picture,place,privacy,promotion_status,properties,shares,source,status_type,story,subscribed,target,targeting,updated_time,type,attachments,to,instagram_eligibility,with_tags&limit=100' % post_from_id)

        if 'data' in posts.keys():
            have_next = True
        else:
            have_next = False
        while have_next:
            have_next = False

            for post in posts['data']:
                post_id = post['id']

                from time import gmtime, strftime
                print("     post_info:", post_id, '  ', strftime("%m-%d %H:%M:%S", gmtime()))

                if post_id in self.post_id_list:
                    continue

                post['post_from_id'] = post_from_id
                if 'created_time' in post.keys():
                    post['created_time'] = change_timezone(post['created_time'])

                if 'updated_time' in post.keys():
                    post['updated_time'] = change_timezone(post['updated_time'])

                try:
                    db.post.insert_one(post)
                except:
                    exception = str(sys.exc_info())
                    db.skipped_table.insert_one(
                        {'post_id': post_id, 'exception': exception, 'other_info': 'post insert_into mongodb'})

                self.post_comments_info(post_id)
                self.post_reactions_info(post_id)

            if 'paging' in posts.keys():
                if 'next' in posts['paging'].keys():
                    try:
                        req = requests.get(posts["paging"]['next'], timeout=7)
                        posts = json.loads(req.text)
                        have_next = True
                    except:
                        exception = str(sys.exc_info())
                        db.skipped_table.insert_one(
                            {'p_page_id': post_from_id, 'exception': exception,
                             'other_info': 'not completed page post'})
                        return 2
                else:
                    pass
            else:
                pass
        return 1

    # Get each post_comment_info for post and insert it to mysql
    @catch_exception(value={'other_info': 'get post comment info'})
    def post_comments_info(self, c_post_id):
        post_comments = self._graph.get_object(
            "%s/comments?fields=attachment,can_comment,can_like,can_remove,is_hidden,like_count,message_tags,user_likes,application,from,id,created_time,message,comment_count,is_private,parent,object&limit=100" % c_post_id)

        print("             comments:", c_post_id)
        if 'data' in post_comments.keys():
            have_next = True
        else:
            have_next = False
        while have_next:
            have_next = False
            # 如果comment_id已经在数据库, 则直接跳过
            for comment in post_comments['data']:
                # 三个长的字典形式统一先处理为字符串形

                # # check comments_id
                # if (comment['id'],) in comments_id_list:
                #     continue

                comment['c_post_id'] = c_post_id
                if 'created_time' in comment.keys():
                    comment['created_time'] = change_timezone(comment['created_time'])

                if 'updated_time' in comment.keys():
                    comment['updated_time'] = change_timezone(comment['updated_time'])

                try:
                    db.post_comment_info.insert_one(comment)
                except:
                    exception = str(sys.exc_info())
                    db.skipped_table.insert_one(
                        {'post_comment_id': comment['id'], 'exception': exception,
                         'other_info': 'post_comment insert_into mongodb'})

            if 'paging' in post_comments.keys():
                if 'next' in post_comments['paging'].keys():
                    try:
                        req = requests.get(post_comments["paging"]['next'], timeout=7)
                        post_comments = json.loads(req.text)
                        have_next = True
                    except:
                        exception = str(sys.exc_info())
                        db.skipped_table.insert_one(
                            {'c_post_id': c_post_id, 'exception': exception,
                             'other_info': 'not completed post comment'})
                else:
                    pass
            else:
                pass

        return 1

    # Get all reactions info of each post and insert it to mysql
    @catch_exception(value={'other_info': 'get post reactions info'})
    def post_reactions_info(self, post_id):

        post_reactions = self._graph.get_object(
            '%s/reactions?fields=can_post,id,link,name,profile_type,username,type,picture{is_silhouette,url}&limit=100&pretty=0' % post_id)

        print("             reactions:", post_id)

        if 'data' in post_reactions.keys():
            have_next = True
        else:
            have_next = False
        while have_next:
            have_next = False
            for reaction in post_reactions['data']:
                if 'type' in reaction.keys():
                    reaction['type_'] = reaction['type']
                reaction['r_post_id'] = post_id

                try:
                    db.post_reaction.insert_one(reaction)
                except:
                    return 2

            if 'paging' in post_reactions.keys():
                if 'next' in post_reactions['paging'].keys():
                    try:
                        req = requests.get(post_reactions["paging"]['next'], timeout=10)
                        post_reactions = json.loads(req.text)
                        have_next = True
                    except:
                        exception = str(sys.exc_info())
                        db.skipped_table.insert_one(
                            {'r_post_id': post_id, 'exception': exception,
                             'other_info': 'not completed post reaction'})
                        print("             reactions not complete:", post_id)
                        return 2
                else:
                    pass
            else:
                pass
        return 1

    @count_time
    def all_info_page(self, page_id):
        t_1 = self.page_info(page_id)  # page_info写入数据库
        if t_1 == 0:  # 判断page_info是否获取成功
            return None
        self.posts_info(page_id)

    # 遍历整个表
    def all_info(self):
        for i in range(self.beg, len(self.df)):
            if pd.isnull(self.df['page_id'][i]):
                self.df['down_record'][i] = -1
                continue

            page_id = str(int(self.df['page_id'][i]))
            self.all_info_page(page_id)

            global beg
            beg = i + 1  # 记录下载到的位置

            self.df['down_record'][i] = 1


def main():
    fb = fbSDK(path='.../1000actor.xlsx')
    fb.all_info()


if __name__ == '__main__':
    main()
