# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader.processors import TakeFirst, Compose, Join


def _generate_tags(values):
    """create a list of tags from `values`"""
    return map(lambda s: s.split(','), values)


class ComicsMetadataScraperItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    image = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    transcript = scrapy.Field(output_processor=TakeFirst())
    creator = scrapy.Field(output_processor=TakeFirst())
    provider = scrapy.Field(output_processor=TakeFirst())
    tags = scrapy.Field(output_processor=Compose(_generate_tags, TakeFirst()))
    url = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    license = scrapy.Field(output_processor=TakeFirst())
