# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LeroymerlinPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy071221

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        item['parameters'] = self.lm_process_parameters(item['parameters'])
        collection.insert_one(item)
        return item

    def lm_process_parameters(self, parameters):
        clear_param = parameters.strip('\n ')
        dict_parameters = dict(zip(clear_param[::2], clear_param[1::2]))
        return dict_parameters

class LeroymerlinPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['pictures']:
            for img in item['pictures']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['pictures'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response, info, item):
        photo_name = str(request.url).split('/')[-1].strip('.jpg')
        product_num = str(item['url']).split('/')[-2].split('-')[-1]
        return f'full/{product_num}/{photo_name}.jpg'
