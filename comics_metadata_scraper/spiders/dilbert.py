# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from comics_metadata_scraper.items import ComicsMetadataScraperItem


class DilbertSpider(scrapy.Spider):
    name = "dilbert"
    domain = "dilbert.com"
    allowed_domains = [domain]
    start_urls = [
        ''.join(['http://', domain, '/'])
    ]

    @classmethod
    def xpath_match_multi_attribute(cls, attr, values):
        return '//*[contains(concat(" ", normalize-space(@{}), " "), " {} ")]'.format(attr, ' '.join(values))

    @classmethod
    def xpath_match_rating(cls):
        return 'div{}//meta/@value'.format(cls.xpath_match_multi_attribute('class', ['js-exp-original']))

    def parse(self, response):
        comics = response.xpath(self.xpath_match_multi_attribute('class', ['comic-item-container']))
        for entry in comics:
            item_loader = ItemLoader(item=ComicsMetadataScraperItem(), response=response)
            item_loader.add_value('provider', self.name)
            item_loader.add_value('id', entry.xpath('@data-id').extract())
            item_loader.add_value('title', entry.xpath('@data-title').extract())
            item_loader.add_value('date', entry.xpath('@data-date').extract())
            item_loader.add_value('image', entry.xpath('@data-image').extract())
            item_loader.add_value('url', entry.xpath('@data-url').extract())
            item_loader.add_value('tags', entry.xpath('@data-tags').extract())
            item_loader.add_value('transcript', entry.xpath('@data-description').extract())
            item_loader.add_value('creator', entry.xpath('@data-creator').extract())
            item_loader.add_value('rating', entry.xpath(self.xpath_match_rating()).extract())
            yield item_loader.load_item()

            next_page = response.xpath('//div[@id="infinite-scrolling"]/a/@href')
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.parse)
