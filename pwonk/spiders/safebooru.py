# -*- coding: utf-8 -*-
import scrapy

from pwonk.items import ImageItem


class SafebooruSpider(scrapy.Spider):
    name = 'safebooru'
    allowed_domains = ['safebooru.org']

    def start_requests(self):
        url = 'https://safebooru.org/index.php?page=post&s=list'
        tags = getattr(self, 'tags', None)
        if tags is not None:
            url = url + '&tags=' + '+'.join(tags.split(',')).strip('+')
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        posts = response.xpath('//*[@id="post-list"]/div[2]/div[1]').xpath('//span//a')
        for post in posts:
            yield response.follow(post, self.parse_post)

        # paginate
        page = [r for r in response.xpath('//*[@id="paginator"]/div/a') if r.xpath('@alt').get() == 'next']

        if len(page) > 0:
            yield response.follow(page[0], self.parse)

    def parse_post(self, response):
        image = response.xpath('//*[@id="image"]/@src').getall()
        yield ImageItem(image_urls=image)
