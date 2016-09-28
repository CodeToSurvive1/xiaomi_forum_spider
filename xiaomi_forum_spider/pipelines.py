# -*- coding: utf-8 -*-

# Define your item pipelines here
# 项目中的pipelines文件.
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
from xiaomi_forum_spider.items import Forum, ForumTheme,ForumThemeComment
import traceback

class XiaomiThemePipeline(object):
    
    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            mysqlHost=crawler.settings.get('MYSQL_HOST'),
            mysqlDbName=crawler.settings.get('MYSQL_DBNAME'),
            mysqlUser=crawler.settings.get('MYSQL_USER'),
            mysqlPasswd=crawler.settings.get('MYSQL_PASSWD'),
            mysqlCharset=crawler.settings.get('MYSQL_CHARSET')
            )

    def __init__(self,mysqlHost,mysqlDbName,mysqlUser,mysqlPasswd,mysqlCharset):
        self.mysqlHost=mysqlHost
        self.mysqlDbName =mysqlDbName
        self.mysqlUser=mysqlUser
        self.mysqlPasswd = mysqlPasswd
        self.mysqlCharset=mysqlCharset

    def open_spider(self, spider):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.conn = MySQLdb.connect(host=self.mysqlHost, user=self.mysqlUser,passwd=self.mysqlPasswd, db=self.mysqlDbName, charset=self.mysqlCharset)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if item.__class__ == Forum:
            sqli = "insert into forum(forum_plates_name,forum_plates_number,forum_plates_url,forum_plates_desc,forum_plates_followed_person_numbers) values(%s,%s,%s,%s,%s)"
            try:
                self.cur.execute(sqli, (
                    item['forumPlatesName'], item['forumPlatesNumber'], item['forumPlatesUrl'], item['forumPlatesDesc'],
                    item['forumPlatesFollowedPersonNumbers']))
                self.conn.commit()
            except Exception as e:
                print traceback.format_exc()
                print '保存论坛板块失败:'+e.message
                self.conn.rollback()

        if item.__class__ == ForumTheme:
            sqli = "insert into forum_theme(theme_number,forum_plate_number,theme_title,theme_creater,theme_creater_id,theme_read_number,theme_reply_number,theme_type,theme_content,theme_create_device) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                self.cur.execute(sqli, (
                    item['themeNumber'],
                    item['forumPlateNumber'], item['themeTitle'], item['themeCreater'], item['themeCreaterId'],
                    item['themeReadNumber'], item['themeReplyNumber'],
                    item['themeType'], item['themeContent'], item['themeCreateDevice']))
                self.conn.commit()
            except:
                print traceback.format_exc()
                print '保存板块主题失败'+item
                self.conn.rollback()

        if item.__class__ == ForumThemeComment:
            sqli = "insert into forum_theme_comment(theme_number,user_id,user_nick_name,user_group,comment_content,comment_time,comment_device_type,comment_floor) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                self.cur.execute(sqli, (
                    item['themeNumber'],
                    item['userId'], item['userNickName'], item['userGroup'], item['commentContent'],item['commentTime'], item['commentDeviceType'],
                    item['commentFloor']))
                self.conn.commit()
            except Exception as e:
                print traceback.format_exc()
                print '保存主题评论失败'+e.message
                self.conn.rollback()
        return item

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()
