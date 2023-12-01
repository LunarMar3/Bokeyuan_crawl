import scrapy
from scrapy import Request

from bokeyuan.items import BokeyuanItem
class MybokeyuanSpider(scrapy.Spider):
    name = "mybokeyuan"
    headers={
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    allowed_domains = ["cnblogs.com"]
    start_urls = ["https://cnblogs.com/sitehome/p/1"]
    global aa
    aa=1
    print("请输入你想要爬取的页数(1-200)")
    global maxinput
    maxinput = int(input())
    if maxinput<1 or maxinput>200:
        maxinput = 1
        print("无效的页数，已设为默认值1")
    
    def parse(self, response):
        global aa
        global maxinput
        articles=response.xpath('//*[@id="post_list"]/article')
        for article in articles:
            article_item=BokeyuanItem()
            article_item["title"]=article.xpath('.//section[@class="post-item-body"]/div[@class="post-item-text"]/a/text()').extract()
            article_item["title_url"]=article.xpath('.//section[@class="post-item-body"]/div[@class="post-item-text"]/a/@href').extract()
            article_item["author"]=article.xpath('.//section[@class="post-item-body"]/footer[@class="post-item-foot"]/a[1]/span/text()').extract()
            article_item["pubtime"]=article.xpath('.//section[@class="post-item-body"]/footer[@class="post-item-foot"]/span[@class="post-meta-item"]/span/text()').extract()
            article_item["support"]=article.xpath('.//section[@class="post-item-body"]/footer[@class="post-item-foot"]/a[2]/span/text()').extract()
            article_item["comments"]=article.xpath('.//section[@class="post-item-body"]/footer[@class="post-item-foot"]/a[3]/span/text()').extract()
            article_item["view"]=article.xpath('.//section[@class="post-item-body"]/footer[@class="post-item-foot"]/a[4]/span/text()').extract()
            yield article_item

        aa+=1
        if aa<=maxinput:
            next_url = 'https://cnblogs.com/sitehome/p/{}'.format(aa)
            yield Request(next_url,headers=self.headers)    



