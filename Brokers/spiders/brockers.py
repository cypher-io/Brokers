# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class BrockersSpider(scrapy.Spider):
    name = "brockers"
    allowed_domains = ["hollard.co.za"]
    start_urls = ['https://www.hollard.co.za/broker-tool']

    def parse(self, response):
        ids = response.xpath('//*[@class="hld-u-1-3 hld-u-md-1-2 hld-u-sm-1-1"]/*[@class="hld-broker-tool-search-results-list-item"]/@data-broker-doc-id').extract()
        location = response.xpath('//*[@class="hld-u-1-3 hld-u-md-1-2 hld-u-sm-1-1"]/*[@class="hld-broker-tool-search-results-list-item"]/@data-location-doc-id').extract()

        dictionary = dict(zip(ids, location))

        for ids, location in dictionary.items():
            absolute_url = 'https://www.hollard.co.za/broker-information?broker='+str(ids)+'&location='+str(location)
            print(absolute_url)

            yield Request(absolute_url, callback=self.parse_page, meta={'URL': absolute_url})

    def parse_page(self, response):
        name = response.xpath('//*[@class="hld-broker-tool-brokerpage-heading-text"]/h3/text()').extract()
        loc = response.xpath('//*[@class="hld-broker-tool-brokerpage-heading-text-location"]/text()').extract()
        offerings = response.xpath('//*[@class="heading"][text()="Our Insurance Product Offerings:"]/following-sibling::p/text()').extract()
        address = response.xpath('//*[@class="heading"][text()="Physical Address:"]/following-sibling::p/text()').extract()
        PO = response.xpath('//*[@class="heading"][text()="Postal Address:"]/following-sibling::p/text()').extract()
        contact = response.xpath('//*[@class="heading"][text()="Contact:"]/following-sibling::p/text()').extract()
        phone = response.xpath('//*[@class="heading"][text()="Phone:"]/following-sibling::p/text()').extract()
        cell = response.xpath('//*[@class="heading"][text()="Cell:"]/following-sibling::p/text()').extract()
        fax = response.xpath('//*[@class="heading"][text()="Fax:"]/following-sibling::p/text()').extract()
        email = response.xpath('//*[@class="heading"][text()="Email:"]/following-sibling::p/a/text()').extract()
        website = response.xpath('//*[@class="heading"][text()="Website:"]/following-sibling::p/a/text()').extract()


        yield{'name': name, 'loc': loc, 'offerings': offerings, 'address': address, 'PO': PO, 'contact': contact, 'phone': phone, 'cell': cell,
              'fax': fax, 'email': email, 'website': website}
