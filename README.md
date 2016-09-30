# xiaomi_forum_spider
小米论坛爬虫

### 软件前提
>需要安装python环境
>pip install scrapy(python版本爬虫)
>pip install MySQL-python(python版本mysql驱动)
>mysql数据库

###数据库表结构设计

####小米论坛板块表forum
```sql
CREATE TABLE `forum` (
  `forum_plates_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '小米论坛板块主键',
  `forum_plates_name` varchar(40) NOT NULL COMMENT '小米论坛板块名称',
  `forum_plates_number` int(11) NOT NULL COMMENT '小米论坛板块编号',
  `forum_plates_url` varchar(256) DEFAULT NULL COMMENT '小米论坛板块访问url',
  `forum_plates_desc` varchar(256) DEFAULT NULL COMMENT '小米论坛板块说明',
  `forum_plates_followed_person_numbers` int(11) NOT NULL COMMENT '板块关注人数',
  PRIMARY KEY (`forum_plates_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='小米论坛板块';

```


####小米论坛主题表forum_theme
```sql
CREATE TABLE `forum_theme` (
  `theme_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主题id',
  `theme_number` int(32) NOT NULL COMMENT '主题编号，理论上不相同',
  `forum_plate_number` int(11) NOT NULL COMMENT '论坛板块编号与forum_plate_number对应',
  `theme_title` varchar(256) DEFAULT NULL COMMENT '主题名称',
  `theme_creater` varchar(256) DEFAULT NULL COMMENT '主题创建者名称',
  `theme_creater_id` int(11) DEFAULT NULL COMMENT '主题创建者id',
  `theme_read_number` int(11) NOT NULL DEFAULT '0' COMMENT '主题阅读人数',
  `theme_reply_number` int(11) NOT NULL DEFAULT '0' COMMENT '主题评论人数',
  `theme_type` varchar(64) NOT NULL COMMENT '主题分类',
  `theme_create_time` varchar(256) DEFAULT NULL COMMENT '主题创建时间',
  `theme_create_device` varchar(256) DEFAULT NULL COMMENT '主题创建设备来源',
  `theme_content` longtext COMMENT '主题内容',
  PRIMARY KEY (`theme_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```


####小米论坛主题评论表forum_theme_comment
```sql
CREATE TABLE `forum_theme_comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `theme_number` int(32) NOT NULL COMMENT '主题编号',
  `user_id` int(11) NOT NULL,
  `user_nick_name` varchar(256) NOT NULL COMMENT '用户昵称',
  `user_group` varchar(256) DEFAULT NULL COMMENT '用户组',
  `comment_content` longblob COMMENT '评论内容',
  `comment_time` datetime DEFAULT NULL COMMENT '评论时间',
  `comment_device_type` varchar(256) DEFAULT NULL COMMENT '评论设备来源',
  `comment_floor` int(11) DEFAULT NULL COMMENT '评论楼层',
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```


####小米论坛用户表user
```sql
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_miid` int(11) NOT NULL,
  `user_group` varchar(256) DEFAULT NULL,
  `user_theme_number` int(11) DEFAULT NULL COMMENT '用户主题数',
  `user_reply_number` int(11) DEFAULT NULL COMMENT '用户回复主题数',
  `user_contribution_value` int(11) DEFAULT NULL COMMENT '贡献值',
  `user_signature` varchar(512) DEFAULT NULL COMMENT '用户个性签名',
  `latest_login_time` datetime DEFAULT NULL COMMENT '最后访问时间',
  `latest_participate_time` datetime DEFAULT NULL COMMENT '上次活动时间',
  `account_register_time` datetime DEFAULT NULL COMMENT '账号注册时间',
  `latest_publish_time` datetime DEFAULT NULL COMMENT '上次发表时间',
  `user_level` varchar(31) DEFAULT NULL COMMENT 'VIP等级',
  `user_vip_number` int(11) DEFAULT NULL COMMENT '第多少位VIP',
  `user_forum_score` int(11) DEFAULT '0' COMMENT '论坛积分',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

###程序启动
```xml
git clone https://github.com/CodeToSurvive1/xiaomi_forum_spider.git
cd xiaomi_forum_spider
scrapy crawl xiaomi-theme
```




