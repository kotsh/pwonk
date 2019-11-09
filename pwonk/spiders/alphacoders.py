# -*- coding: utf-8 -*-
import scrapy

from pwonk.items import ImageItem


class AlphacodersSpider(scrapy.Spider):
    name = 'alphacoders'
    allowed_domains = ['wall.alphacoders.com']

    def start_requests(self):
        url = 'https://wall.alphacoders.com/search.php'
        search = getattr(self, 'search', None)
        if search is not None:
            url = url + '?search=' + '+'.join(search.split(' ')).strip('+')
        else:
            raise ValueError('You must input a search term!')
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        posts = response.xpath('/html/body/div[2]/div[5]/div/div[1]/div[1]/a/@href').getall()
        for post in posts:
            yield response.follow(post, self.parse_post)

        # pagination
        pagination = response.xpath('//*[@id="next_page"]/@href').getall()
        if len(pagination) > 0:
            if pagination != '#':
                yield response.follow(pagination[0], self.parse)

    def parse_post(self, response):
        yield ImageItem(image_urls=response.xpath('/html/body/div[2]/div[4]/a/@href').getall())
