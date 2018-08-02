# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class McrawlPipeline(object):
    def process_item(self, item, spider):
        return item

import scrapy
from scrapy.pipelines.images import FilesPipeline
from scrapy.exceptions import DropItem
from PIL import Image

class MyFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'filename': item['num_cat'] + '/' + item['id'] + '.jpg'})


    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename','')

    def item_completed(self, results, item, info):
        for result, image_info in results:
            if result:
                path = image_info['path']
                img = Image.open('img/' + path)
                # here is where you do your resizing - this method overwrites the
                # original image you will need to create a copy if you want to keep
                # the original.
                scale = 300 / min(img.size[0],img.size[1])
                img = img.resize((max(300, int(scale * img.size[0])), max(300, int(scale * img.size[1]))))
                img.save('img/' + path)
        return item
