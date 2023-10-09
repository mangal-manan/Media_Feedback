import scrapy
from pathlib import Path
from ..items import MongoDbItem
import pymongo

class ListNdtvSpider(scrapy.Spider):
    name = "list_ndtv"
    allowed_domains = ["www.ndtv.com"]
    start_urls = ["https://www.ndtv.com/india"]
    next_page_number = 2
    stored_set = set()

    def __init__(self, *args, **kwargs):
        super(ListNdtvSpider, self).__init__(*args, **kwargs)
        self.pages_followed = 0
        self.pageno = 1
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["items"]
        col = db["Data"]
        x = col.find()
        for data in x:
            self.stored_set.add(data["ID"])

    def parse(self, response):
        for href in response.css("div .news_Itm-img a::attr(href)"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)
        index = 0
        next_url = self.start_urls[0] + "/page-" + str(self.next_page_number)
        self.next_page_number += 1
        if self.next_page_number >= 25:
            print("?????????Limit reached???????????")
            return
        print("-" * 20)
        print(next_url)
        print("-" * 20)
        yield scrapy.Request(next_url, callback = self.parse)

    def parse_dir_contents(self, response):
        item = MongoDbItem()
        item['ID'] = response.url[len(response.url) - 7:]
        if item['ID'] in self.stored_set:
            return
        self.stored_set.add(item['ID'])
        metadata = ""
        resp = list(response.css("html body div section div div div div div p::text").getall())
        for line in resp:
            metadata += line + " "
        item['Metadata'] = metadata
        arr = response.xpath('//span[contains(@itemprop, "date")]/text()').get().split(" ")
        if(arr[-2] == "am"):
            item['Time'] = arr[-3]
        else:
            item['Time'] = str(int(arr[-3][0]) + 12) + arr[-3][-3:]
        item['Date'] = arr[1] + " " +  arr[2] +" " +arr[3]
        item['Website'] = "NDTV"
        item['URL'] = response.url
        item['Language'] = "English"
        yield item
