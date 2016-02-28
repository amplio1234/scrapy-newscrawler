from scrapy import Spider
from scrapy.spiders import Rule
#from scrapy.selector import Selector
from smh.items import SmhItem
from scrapy.linkextractors import LinkExtractor

class smhSpider(Spider):
    name="smh"
    allowed_domains=["www.smh.com.au"]
    start_urls=["http://www.smh.com.au/federal-politics/political-news",]


    rules = [
                Rule(LinkExtractor(allow=r'federal-politics/political-news'),
                             callback='parse', follow=True)
                ]
    
    def parse(self, response):
        newsCollection = response.xpath('//div[@class="wof"]')

        for news in newsCollection:
            item=SmhItem()
            try:
                item['title']=news.xpath(
                        'h3/a/@title').extract()[0]
                item['url']=news.xpath(
                        'h3/a/@href').extract()[0]
                item['author']=news.xpath('p/cite/a/text()').extract()[0]
                item['abstract']=news.xpath(
                        'p/text()').extract()[1].replace('\n','').rstrip().lstrip()
                yield item
            except Exception as exc:
                self.log("item filling exception: %s" % exc)
                continue
