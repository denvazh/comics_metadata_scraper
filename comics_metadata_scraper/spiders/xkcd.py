# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from comics_metadata_scraper.items import ComicsMetadataScraperItem


class XkcdSpider(scrapy.Spider):
    name = "xkcd"
    domain = "xkcd.com"
    allowed_domains = [domain]
    start_urls = [
        ''.join(['http://', domain, '/'])
    ]

    @classmethod
    def fetch_urls(cls, entries):
        return filter(lambda s: s, map(lambda s: cls.remove_whitespaces(s), set(entries)))

    @classmethod
    def fetch_entry(cls, entries, condition_str):
        matches = filter(lambda s: s.startswith(condition_str), cls.fetch_urls(entries))
        if not matches:
            return []
        else:
            return map(lambda s: s.split(': ')[1], matches)[0]

    @classmethod
    def remove_whitespaces(cls, src_str):
        import string
        return src_str.strip(string.whitespace)

    def parse(self, response):
        middle_container = response.xpath('//div[@id="middleContainer"]/text()')
        url = self.fetch_entry(middle_container.extract(), 'Permanent link')
        image = self.fetch_entry(middle_container.extract(), 'Image URL')

        # need only one because there is only one comic per page
        item_loader = ItemLoader(item=ComicsMetadataScraperItem(), response=response)
        item_loader.add_value('provider', self.name)
        item_loader.add_value('id', url.replace('http://' + self.allowed_domains[0], '').replace('/', ''))
        item_loader.add_value('creator', 'Randall Munroe')
        item_loader.add_xpath('title', '//div[@id="middleContainer"]/div[@id="ctitle"]/text()')
        item_loader.add_value('url', url)
        item_loader.add_value('image', image)
        item_loader.add_xpath('transcript', '//div[@id="transcript"]/text()')
        item_loader.add_xpath('license', '//div[@id="licenseText"]/p/a/@href')
        yield item_loader.load_item()

        # pagination
        next_page = response.xpath('//ul[@class="comicNav"][1]/li/a[@rel="prev"]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
