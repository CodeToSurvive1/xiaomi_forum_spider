# -*- coding: utf-8 -*-

import redis
from tutorial.utils.MySqlDaoUtil import MySqlDaoUtil

class RedisUtil:
    
    #服务加载启动后，将所有的论坛板块url及对应的id加载到redis中
    @classmethod
    def forum_list_to_redis(cls):
        r = redis.Redis(host='localhost',port=6379,db=0)
        dao = MySqlDaoUtil()
        forumResult = dao.query_all_forums()
        ##设置url为主键，id为值的map结构
        for line in forumResult:
            key = line[2]
            value = line[0]
            r.set(key,value)

    #根据url获取其id
    @classmethod
    def get_forum_id_by_url(cls,url):
        r = redis.Redis(host='localhost',port=6379,db=0)
        return r.get(url)

    #将key，value键值对放到redis缓存中
    @classmethod
    def put_key_and_value(cls,key,value):
        r = redis.Redis(host='localhost',port=6379,db=0)
        r.set(key,value)
