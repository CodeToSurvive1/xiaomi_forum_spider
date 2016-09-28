# -*- coding: utf-8 -*-
import scrapy
from xiaomi_forum_spider.items import Forum
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from xiaomi_forum_spider.items import ForumTheme,ForumThemeComment
import urlparse
import time,datetime
import traceback


class XiaomiSpider(CrawlSpider):
    name = "xiaomi-theme"
    allowed_domains = ["xiaomi.cn"]
    start_urls = ["http://www.xiaomi.cn/index.html"]
    # start_urls = ["http://bbs.xiaomi.cn/t-13161707"]
    theme_url = "http://bbs.xiaomi.cn"


    #抓取主页的论坛板块链接
    def parse(self, response):
        
        for line in response.css('.header_menu_list>ul>li>a'):
            url = line.xpath('@href').extract()[0].encode('utf-8')

            #获取论坛编号
            try:
                number = int(url.split('-')[len(url.split('-')) - 1])
            except:
                number = int(url.split('/')[len(url.split('/')) - 1])
            finally:
                request = scrapy.Request(url,callback=self.parse_forum)
                request.meta['number']=number
                yield request

                #由于上面请求url与这里的请求url相同，因此添加参数dont_filter=True，也就是不会进行相同url拦截不进入队列的设置
                '''也就是说无论url是否之前已经进入过队列，都会重新进入队列中重新排队'''
                request = scrapy.Request(url,callback=self.parse_forum_theme,dont_filter=True)
                request.meta['number']=number
                yield request
    
    #抓取forum论坛板块表信息，主表forum
    def parse_forum(self, response):
        #论坛板块名称，如果没有名称，直接跳过不进行相关数据解析
        name = response.css('.contain_header_con > div > a > h2::text').extract()
        if name:
            forum = Forum()

            #名称
            forumName = name[0].encode('utf-8')
            forum['forumPlatesName'] = forumName

            #url
            formUrl = response.url
            forum['forumPlatesUrl'] = formUrl

            #论坛编号
            forum['forumPlatesNumber'] = response.meta['number']

            #描述
            desc = response.css('.intro::text')
            if desc:
                forumPlatesDesc = desc.extract()[0].encode('utf-8')
                forum['forumPlatesDesc'] = forumPlatesDesc
            else:
                 forum['forumPlatesDesc'] =''
            
            #论坛关注人数
            number = response.css('.num::text').extract()
            if number:
                forumPlatesFollowedPersonNumbers = number[0].encode('utf-8')
                forum['forumPlatesFollowedPersonNumbers'] = forumPlatesFollowedPersonNumbers
            else:
                forum['forumPlatesFollowedPersonNumbers'] = 0

            #返回组装数据后会调用pipelines中的方法
            yield forum

    #根据论坛板块链接抓取该板块的所有链接，包括分页
    def parse_forum_theme(self, response):

        '''获取当前页面上的主题 '''
        self.log("获取论坛页面链接为" + response.url)

        theme_list = response.xpath('//body/div[1]/div[3]/div[3]/div/div[2]/ul/li')
        for theme in theme_list:
            themeTitle = theme.xpath('div[2]/div[1]/a/text()').extract()[0]
            if (themeTitle == ''):
                continue
            url = urlparse.urljoin(self.theme_url, theme.xpath('div[2]/div[1]/a/@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_theme,meta={'number':response.meta['number']})

        # '''获取当前页面上的主题 '''
        next_pages = response.css('.next').xpath('./a/@href')

        '''若存在下一页主题,则递归爬取每页信息'''
        if next_pages:
            next_page = urlparse.urljoin(self.theme_url, next_pages[0].extract())
            yield scrapy.Request(next_page, callback=self.parse_forum_theme,
                                    meta={'number':response.meta['number']})

    def parse_theme(self, response):
        self.log("当期主题页面链接为" + response.url)
        themePage = response.xpath('//body/div[1]/div[3]/div[3]/div[1]/div[1]')
        forumTheme = ForumTheme()
        forumTheme['themeTitle'] = themePage.xpath('h1/span[3]/text()').extract()[0].encode('utf-8')
        # forumTheme['themeCreateTime'] = themePage.xpath('p/span[3]/text()').extract()[0].encode('utf-8')
        forumTheme['themeType'] = themePage.xpath('p/a[1]/text()').extract()[0].encode('utf-8')
        forumTheme['themeReadNumber'] = \
            response.xpath('//body/div[1]/div[3]/div[3]/div[1]/div[1]/p/span[last()]/text()').extract()[0].encode(
                'utf-8')
        forumTheme['themeReplyNumber'] = \
            themePage.xpath('//body/div[1]/div[3]/div[3]/div[1]/div[1]/p/span[last()-1]/text()').extract()[0].encode(
                'utf-8')
        forumTheme['themeContent'] = themePage.css('.invitation_content').extract()[0].encode('utf-8')
        forumTheme['themeCreateDevice'] = themePage.xpath('p/a[1]/text()').extract()[0].encode('utf-8')

        forumTheme['themeCreater'] = \
            response.xpath('//body/div[1]/div[3]/div[2]/div[1]/div/div/div/span/a/text()').extract()[0].encode('utf-8')

        forumTheme['themeCreaterId'] = \
            response.xpath('//body/div[1]/div[3]/div[2]/div[1]/div/div/div/span/a/@u-id').extract()[0].encode('utf-8')

        forumTheme['forumPlateNumber'] = response.meta['number']

        themeNumber = response.xpath('//body/div[1]/div[3]/div[3]/div[1]/@date-id').extract()[0].encode('utf-8')
        forumTheme['themeNumber'] = themeNumber

        yield forumTheme
        
        # 解析每页上的评论信息
        response.meta['themeNumber']=themeNumber

        comments = self.parse_comment_page(response)
        yield comments
        #获取评论的翻页信息
        next_pages = response.css('.next').xpath('./a/@href')

        '''若存在下一页评论,则递归爬取每页信息'''
        if next_pages:
            next_page = urlparse.urljoin(self.theme_url, next_pages[0].extract())
            yield scrapy.Request(next_page, callback=self.parse_comment_page,
                meta={'themeNumber':themeNumber})


    def parse_comment_page(self,response):
        comments=[]
        for commentLine in response.css('.reply_list > li'):
            content = commentLine.css('.reply_txt')
            if content:
                comment = ForumThemeComment()
                comment['userId'] = commentLine.xpath('@u-id').extract()[0].encode('utf-8')
                comment['userNickName'] = commentLine.css('.auth_name::text').extract()[0].encode('utf-8')
                comment['userGroup'] = commentLine.xpath('div[2]/div[1]/span[1]/text()').extract()[0].encode('utf-8')
                comment['commentContent'] = content.extract()[0].encode('utf-8')

                timeStr = commentLine.xpath('div[2]/div[1]/span[3]/text()').extract()
                if timeStr:
                    timeOrig = timeStr[0].encode('utf-8')
                    if '刚刚' in timeOrig:
                        timeReal = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    elif '分钟前' in timeOrig:
                        timeReal = (datetime.datetime.now() - datetime.timedelta(minute = timeOrig.rstrip('分钟前')))
                    elif '小时前' in timeOrig:
                        timeReal = (datetime.datetime.now() - datetime.timedelta(hour = timeOrig.rstrip('小时前')))
                    elif '天前' in timeOrig:
                        timeReal = (datetime.datetime.now() - datetime.timedelta(day = timeOrig.rstrip('天前')))
                    else:
                        try:
                            timeReal = time.strptime(timeOrig, "%Y-%m-%d %H:%M:%S")
                        except:
                            print timeOrig
                            year = time.strftime('%Y',time.localtime(time.time()))
                            timeNew = year+'-'+timeOrig
                            print timeNew
                            timeReal = time.strptime(timeNew, "%Y-%m-%d %H:%M:%S")
                            print timeReal
                            timeReal = time.strftime("%Y-%m-%d %H:%M:%S",timeReal)
                    comment['commentTime'] = timeReal

                comment['commentDeviceType'] = commentLine.xpath('div[2]/div[1]/span[4]/text()').extract()[0].encode('utf-8')

                floor = commentLine.css('.reply_list_float::text').extract()
                if floor:
                    floorNumber = floor[0].encode('utf-8').rstrip('#')
                    if '地板' in floorNumber:
                         comment['commentFloor'] = '3'
                    elif '板凳' in floorNumber:
                        comment['commentFloor'] = '2'
                    elif '沙发' in floorNumber:
                        comment['commentFloor'] ='1'
                    else:
                        comment['commentFloor'] = floorNumber
                
                themeNumber = response.meta['themeNumber']
                if themeNumber:
                    comment['themeNumber'] = themeNumber
                comments.append(comment)
        return comments
