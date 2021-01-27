import scrapy
import requests
from TiebaSpider.items import TiebaspiderItem


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/m?kw=林允儿&pn=0']

    def parse(self, response):
        div_list = response.xpath("//div[contains(@class,'i')]")
        for div in div_list:
            item = TiebaspiderItem()
            item["title"] = div.xpath(".//a/text()").extract_first()
            item["href"] = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/" + div.xpath(".//a/@href").extract_first()
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/" + next_url,
                callback=self.parse)


    def parse_detail(self, response):
        item = response.meta["item"]
        div_list = response.xpath("//div[@class='i']")
        for div in div_list:
            item["content"] = div.xpath("./text()").extract_first()
            item["content_img"] = div.xpath(".//img/@src").extract()
            item["content_img"] = [requests.utils.unquote(i).split("src=")[-1] for i in item["content_img"]]
            yield item
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
             yield scrapy.Request(
                 "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/" + next_url,
                 callback=self.parse_detail，
                 meta={'item': item}
                 )
             
