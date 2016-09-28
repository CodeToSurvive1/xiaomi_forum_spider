# -*- coding: utf-8 -*-
import sys
import MySQLdb
from tutorial.items import Forum, ForumTheme

class MySqlDaoUtil(object):

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.conn = MySQLdb.connect(host='localhost', user='root',passwd='123456', db='xiaomi_forum', charset='utf8')
        self.cur = self.conn.cursor()

    def query_all_forums(self):
        sqli = "select forum_plates_id,forum_plates_name,forum_plates_url,forum_plates_followed_person_numbers,forum_plates_desc from forum "
        self.cur.execute(sqli)
        results = self.cur.fetchall()
        return results



