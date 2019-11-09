# -*- coding: utf-8 -*-
import scrapy

from pwonk.items import ImageItem


class YandereSpider(scrapy.Spider):
    name = 'yandere'
    allowed_domains = ['yande.re']

    def start_requests(self):
        url = 'https://yande.re/post'
        tags = getattr(self, 'tags', None)
        if tags is not None:
            url = url + '?tags=' + '+'.join(tags.split(',')).strip('+')
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        posts = response.xpath('//*[@id="post-list-posts"]').xpath('//li//div//a/@href').getall()
        for post in posts:
            yield response.follow(post, self.parse_post)

        # paginate
        page = response.xpath('//*[@id="paginator-next"]')

        if len(page) > 0:
            yield response.follow(page[0], self.parse)

    def parse_post(self, response):
        larger = response.xpath('//*[@id="highres"]/@href').getall()
        if len(larger) > 0:
            self.logger.info('Found highres, fetching that instead.')
            yield ImageItem(image_urls=larger)
        else:
            image = response.xpath('//*[@id="image"]/@src').getall()
            yield ImageItem(image_urls=image)
