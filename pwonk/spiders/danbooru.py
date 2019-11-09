# -*- coding: utf-8 -*-
import scrapy

from pwonk.items import ImageItem


class DanbooruSpider(scrapy.Spider):
    name = 'danbooru'
    allowed_domains = ['danbooru.donmai.us']

    def start_requests(self):
        url = 'https://danbooru.donmai.us/posts'
        tags = getattr(self, 'tags', None)
        if tags is not None:
            url = url + '?tags=' + '+'.join(tags.split(',')).strip('+')
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        posts = response.xpath('//*[@id="posts-container"]')
        if len(posts) > 0:
            yield ImageItem(image_urls=posts.xpath('//article/@data-file-url').getall())

        # paginate
        page = response.xpath('//*[@id="paginator-next"]')

        if len(page) > 0:
            yield response.follow(page[0], self.parse)
