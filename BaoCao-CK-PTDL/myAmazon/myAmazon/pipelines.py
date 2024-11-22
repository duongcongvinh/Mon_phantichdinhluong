# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# import các thư viện cần thiết
from itemadapter import ItemAdapter
import scrapy  # thư viện này để thực hiện việc thu thập dữ liệu từ web
import pymongo  # thư viện để 'kêts nối với MongoDB
from pymongo import MongoClient  # sử dụng để kết nối với MongoDB
import json  # xử lý dữ liệu JSON
import csv  # xử lý dữ liệu CSV
from scrapy.exceptions import DropItem  # để loại bỏ các mục không hợp lệ
import os  # để làm việc với các biến môi trường



import pymongo  # Library to connect with MongoD
from pymongo import MongoClient  # Used for connecting to MongoDB
# Pipeline to store data into MongoDB
class MongoDBAmazon1Pipeline:
    def __init__(self):
        # Initialize the connection to MongoDB
        econnect = os.environ.get('Mongo_HOST', 'localhost')  # Use 'localhost' if 'Mongo_HOST' is not set
        try:
            # Connect to MongoDB
            self.client = pymongo.MongoClient(f'mongodb://{econnect}:27017')
            self.db = self.client['dbAmazon']  # Create or connect to the database 'dbAmazon'
        except Exception as e:
            raise Exception(f"Không thể kết nối đến MongoDB: {e}") 
    
    def process_item(self, item, spider):
        # Process each collected item
        collection = self.db['tbl_CrawlerAmazon']  # Create or connect to the collection
        try:
            collection.insert_one(dict(item))  # Convert the item to a dictionary and insert into the collection
            return item  
        except Exception as e:
            raise DropItem(f"Lỗi khi chèn item vào MongoDB: {e}")  

# Pipeline để lưu trữ dữ liệu vào file JSON
class JsonDBAmazon1Pipeline:
    def process_item(self, item, spider):
        # Xử lý từng mục và lưu vào file JSON
        with open('dataAmazon.json', 'a', encoding='utf-8') as file:  # Mở file JSON ở chế độ ghi thêm
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'  # Chuyển item thành chuỗi JSON
            file.write(line)  # Ghi chuỗi JSON vào file
        return item

# Pipeline để lưu trữ dữ liệu vào file CSV
class CSVDBAmazon1Pipeline:
    def process_item(self, item, spider):
        # Mở file CSV và ghi dữ liệu vào
        with open('dataAmazon.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='$')  # Sử dụng ký tự '$' làm dấu phân cách
            writer.writerow([
                item.get('productName', 'N/A'),  # Nếu không có giá trị, trả về 'N/A'
                item.get('brand', 'N/A'),
                item.get('price', 'N/A'),
                item.get('fabricType', 'N/A'),
                item.get('closureType', 'N/A'),
                item.get('countryOfOrigin', 'N/A'),
                item.get('customerssay', 'N/A'),
                item.get('productDescription', 'N/A'),
                item.get('ratings', 'N/A'),
                item.get('rate', 'N/A'),
                item.get('about', 'N/A'),
            ])
        return item