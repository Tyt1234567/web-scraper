import asyncio
import aiohttp
import logging
import json
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s:%(message)s')
index_url='https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
detail_url='https://spa5.scrape.center/api/book/{id}'
page_size=18
page_number=500
concurrency=10

#爬取页
semaphore=asyncio.Semaphore(concurrency)
session=None
async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s',url)
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s',url,exc_info=True)

#爬取列表页
async def scrape_index(page):
    url=index_url.format(offset=page_size*(page-1))
    return await scrape_api(url)

#MongoDB存储
MONGO_CONNECTION_STRING='mongodb://localhost:27017'
MONGO_DB_NAME='books'
MONGO_COLLECTION_NAME='books'
client=AsyncIOMotorClient(MNGO_CONNECTION_STRING)
db=client[MONGO_DB_NAME]
collection=db[MONGO_COLLECTION_NAME]

async def scrape_detail(id):
    url=detail_url.format(id=id)
    data=await scrape_api(url)
    await save_data(data)


async def save_data(data):
    logging.info('save data %s',data)
    if data:
        return await collection.update_one(
            {'id':data.get('id')},
            {'$set':data},
            upsert=True
        )

async def main():
    global session
    session=aiohttp.ClientSession()
    scrape_index_task=[asyncio.ensure_future(scrape_index(page)) for page in range(1,page_number+1)]
    results=await asyncio.gather(*scrape_index_task)
    logging.info('result %s',json.dumps(results,ensure_ascii=False, indent=2))

    ids=[]
    for index_data in results:
        if not index_data:
            continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    scrape_details_task=[asyncio.ensure_future(scrape_detail(id)) for id in ids]
    await asyncio.wait(scrape_details_task)
    await session.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())