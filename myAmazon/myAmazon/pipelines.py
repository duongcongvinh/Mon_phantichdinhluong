# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import scrapy
import pymongo 
from pymongo import MongoClient
import json
import csv
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class MongoDBAmazon1Pipeline:
    def __init__(self):
        # connection String
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['db_CrawlerAmazon'] # Create Database      
        pass
    
    def process_item(self, item, spider):
        
        collection =self.db['tbl_CrawlerAmazon'] # Create Colecction or Table
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")       
        pass 

class JsonDBAmazon1Pipeline:
    def process_item(self, item, spider):
        with open('dataAmazon.json', 'a', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(line)
        return item
    

class CSVDBAmazon1Pipeline:
    def process_item(self, item, spider):
        with open('dataAmazon.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='$')
            writer.writerow([
                item['productName'],
                item['brand'],
                item['price'],
                item['fabricType'],
                item['closureType'],
                item['countryOfOrigin'], 
                item['describe'],
                item['productDescription'],
                item['ratings'], 
                item['rate'],
            ])
        return item
    pass