import requests
import logging
import pymongo
from tqdm import tqdm

logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s:%(message)s')
index_url='https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'

#通过Ajax接口爬取
def scrape_api(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    logging.info('scraping %s...',url)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()     #专门用于处理JSON接口，解析相应内容并转化为JSON字符串
        else:
            logging.error('get invaild status code %s while scraping %s',response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

#目录页
LIMIT=10
def scrape_index(page):
    url = index_url.format(limit=LIMIT,offset=LIMIT*(page-1))
    return scrape_api(url)

#单独电影页
detail_url='https://spa1.scrape.center/api/movie/{id}'
def scrape_detail(id):
    url=detail_url.format(id=id)
    return scrape_api(url)

#保存数据（MongoDB）
mongo_db_name='movies'
mongo_collection_name='movies'
client=pymongo.MongoClient(host='localhost',port=27017)
db=client['movies']
collection=db['movies']
def save_data(data):
    collection.update_one(
        {'name' : data.get('name')},
        {"$set" : data},
        upsert=True
    )

total_page=10
def main():
    for page in tqdm(range(1,total_page+1)):
        index_data=scrape_index(page)#目录页
        for item in index_data.get('results'):
            id=item.get('id')
            detail_data=scrape_detail(id)
            logging.info('detail data %s', detail_data)
            save_data(detail_data)
            logging.info('data saved successfully')

if __name__ =='__main__':
    main()