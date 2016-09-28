# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 项目中的item文件
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# `forum_ plates` varchar(40) NOT NULL COMMENT '小米论坛板块名称',
# `forum_plates_number` int(11) NOT NULL COMMENT '小米论坛板块编号',
# `forum_plates_url` varchar(256) DEFAULT NULL COMMENT '小米论坛板块访问url',
# `forum_plates_desc` varchar(256) DEFAULT NULL COMMENT '小米论坛板块说明',
# `forum_plates_followed_person_numbers` int(11) NOT NULL COMMENT '板块关注人数',
# PRIMARY KEY (`forum_plates_id`)


class Forum(scrapy.Item):
    # forumPlatesId = scrapy.Field()
    forumPlatesName = scrapy.Field()
    forumPlatesNumber = scrapy.Field()
    forumPlatesUrl = scrapy.Field()
    forumPlatesDesc = scrapy.Field()
    forumPlatesFollowedPersonNumbers = scrapy.Field()


#   `theme_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主题id',
#   `theme_number` INT(32) NOT NULL COMMENT 主题编号，理论上不相同,
#   `forum_plate_number` int(11) NOT NULL COMMENT '论坛板块编号与forum_plate_number对应',
#   `theme_title` varchar(256) NOT NULL COMMENT '主题名称',
#   `theme_creater` varchar(256) DEFAULT NULL COMMENT '主题创建者名称',
#   `theme_creater_id` int(11) DEFAULT NULL COMMENT '主题创建者id',
#   `theme_read_number` int(11) NOT NULL DEFAULT '0' COMMENT '主题阅读人数',
#   `theme_reply_number` int(11) NOT NULL DEFAULT '0' COMMENT '主题评论人数',
#   `theme_type` varchar(64) NOT NULL COMMENT '主题分类',
#   `theme_content` longtext NOT NULL COMMENT '主题内容',
#   `theme_create_time` datetime DEFAULT NULL COMMENT '主题创建时间',
#   `theme_create_device` varchar(256) DEFAULT NULL COMMENT '主题创建设备来源',
class ForumTheme(scrapy.Item):
    # themeId = scrapy.Field()
    themeNumber = scrapy.Field()
    forumPlateNumber = scrapy.Field()
    themeTitle = scrapy.Field()
    themeCreater = scrapy.Field()
    themeCreaterId = scrapy.Field()
    themeReadNumber = scrapy.Field()
    themeReplyNumber = scrapy.Field()
    themeType = scrapy.Field()
    themeContent = scrapy.Field()
    themeCreateTime = scrapy.Field()
    themeCreateDevice = scrapy.Field()

#   `comment_id` int(11) NOT NULL,
#   `theme_number` INT(32) NOT NULL COMMENT 主题编号,
#   `user_id` int(11) NOT NULL,
#   `user_nick_name` varchar(256) NOT NULL COMMENT '用户昵称',
#   `user_group` varchar(256) DEFAULT NULL COMMENT '用户组',
#   `comment_content` varchar(255) DEFAULT NULL COMMENT '评论内容',
#   `comment_time` datetime DEFAULT NULL COMMENT '评论时间',
#   `comment_device_type` varchar(256) DEFAULT NULL COMMENT '评论设备来源',
#   `comment_floor` int(11) DEFAULT NULL COMMENT '评论楼层',
class ForumThemeComment(scrapy.Item):
    # commentId = scrapy.Field()
    themeNumber = scrapy.Field()
    userId = scrapy.Field()
    userNickName = scrapy.Field()
    userGroup = scrapy.Field()
    commentContent = scrapy.Field()
    commentTime = scrapy.Field()
    commentDeviceType = scrapy.Field()
    commentFloor = scrapy.Field()
