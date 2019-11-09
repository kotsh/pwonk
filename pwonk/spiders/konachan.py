# -*- coding: utf-8 -*-
import scrapy

from pwonk.items import ImageItem


class KonachanSpider(scrapy.Spider):
    name = 'konachan'
    allowed_domains = ['konachan.com']

    def start_requests(self):
        url = 'https://konachan.com/post'
        tags = getattr(self, 'tags', None)
        if tags is not None:
            url = url + '?tags=' + '+'.join(tags.split(',')).strip('+')
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        posts = response.xpath('//*[@id="post-list-posts"]').xpath('//li//div//a')
        for post in posts:
            yield response.follow(post, self.parse_post)

        # paginate
        page = [r for r in response.xpath('/html/body/div[7]/div[1]/div[3]/div[5]/div') if r.xpath('@rel').get() == 'next']

        if len(page) > 0:
            yield response.follow(page[0], self.parse)

    def parse_post(self, response):
        image = response.xpath('//*[@id="image"]/@src').getall()
        yield ImageItem(image_urls=image)
