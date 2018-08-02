# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import scrapy
from scrapy.http import Request
from mcrawl.items import McrawlItem


class MercariSpider(scrapy.Spider):
    name = 'mercari'
    allowed_domains = ['mercari.com']
    start_urls = ['https://www.mercari.com/category/']

    def __init__(self, ppc=100, start_cat=149, finish_cat=1559, *args, **kwargs):
        super(MercariSpider, self).__init__(*args, **kwargs)
        self.pages_per_category = int(ppc)
        self.start_cat = int(start_cat)
        self.finish_cat = int(finish_cat)

    def parse(self, response):
        urls = response.css('.category-list-box').css('a').xpath('@href').extract()
        urls = [url.split('/')[-2] for url in urls if (int(url.split('/')[-2]) >= self.start_cat) and (int(url.split('/')[-2]) <= self.finish_cat)]
        for url in urls:
            yield Request(urljoin(response.url, url), callback=self.parse_section)

    def parse_section(self, response):
        try:
            num_pages = response.css('.pagination-wrapper').css('a').xpath('@href').extract()[-1]
            num_pages = int(num_pages.split('=')[1])
        except:
            num_pages=1
        for i in range(1, min(num_pages, self.pages_per_category)+1):
            next_page = urljoin(response.url, '?page={}'.format(i))
            yield Request(next_page, callback=self.parse_section_page,
                          meta={'num_cat': response.url.split('/')[-2]})

    def parse_section_page(self, response):
        urls = response.css('.product-grid-container').css('a').xpath('@href').extract()
        for url in urls:
            yield Request(url, callback=self.parse_product,
                          meta={'num_cat': response.meta.get('num_cat','')})

    def parse_product(self, response):
        pbox = response.css('.item-container-inner')
        stats = pbox.css('.item-column-right')
        if len(stats.css('.item-detail-list')) > 1:
            categories = stats.css('.item-detail-list')[0].css('a').xpath('text()').extract()
            brands = stats.css('.item-detail-list')[1].css('a').xpath('text()').extract()
        else:
            categories = stats.css('.item-detail-list')[0].css('a').xpath('text()').extract()
            brands = None
        dpref = stats.css('.item-description').css('p').xpath('text()').extract()
        dsuff = stats.css('.item-description').css('span').xpath('text()').extract()
        # build Product item
        product = McrawlItem()
        product['name'] = stats.css('.item-body').css('h2').xpath('text()').extract()[0]
        product['price'] = stats.css('.item-price').css('h3').xpath('text()').extract()[0]
        product['condition'] = stats.css('.item-status-list').css('p').xpath('text()').extract()[0]
        product['size'] = stats.css('.item-status-list').css('p').xpath('text()').extract()[1]
        product['shipping'] = stats.css('.item-status-list').css('p').xpath('text()').extract()[2]
        product['description'] = ''.join(map(lambda x: x.strip(' \n\t'), dpref + dsuff))
        product['categories'] = '/'.join(map(lambda x: x.strip(' \n\t'), categories))
        product['brand'] = '' if not brands else '/'.join(map(lambda x: x.strip(' \n\t'), brands))
        product['image'] = pbox.css('.item-column-left').css('.item-photos').css('.owl-item-inner').css('img').xpath('@src').extract()[0].split('?')[0]
        product['file_urls'] =  [product['image']]
        product['url'] = response.url
        product['id'] = response.url.split('/')[-2]
        product['num_cat'] = response.meta.get('num_cat','')
        yield product
