import multiprocessing
import requests
import logging
import re
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists


logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(levelname)s:%(message)s')
base_url='https://ssr1.scrape.center'
total_page=10

#获取任意网页源代码
def scrape_page(url):
    logging.info('scraping %s...',url)
    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logging.error('get invaild status code %s while scraping %s',response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)

#获取每页源代码
def scrape_index(page):
    index_url=f'{base_url}/page/{page}'
    return scrape_page(index_url)

#找到网页中所有符合条件的超链接地址
def parse_index(html):
    pattern=re.compile('<a.*?href="(.*?)".*?class="name">')
    items=re.findall(pattern,html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(base_url, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url

#获取详细页面源代码
def scrape_detail(url):
    return scrape_page(url)

#解析详情页
def parse_detail(html):
    cover_pattern=re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">',re.S)
    name_pattern=re.compile('<h2.*?>(.*?)</h2>')

    if re.search(cover_pattern,html):
        cover=re.search(cover_pattern,html).group(1).strip()
    else:
        None
    if re.search(name_pattern,html):
        name=re.search(name_pattern,html).group(1).strip()
    else:
        None

    return {
        'cover':cover,
        'name':name,
    }

#创建或打开文件夹储存数据
result_dir='result'
exists(result_dir) or makedirs(result_dir)

#储存数据
def save_data(data):
    name=data.get('name')
    path=f'{result_dir}/{name}.json'
    json.dump(data,open(path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

#执行程序
def main(page):
    index_html=scrape_index(page)
    detail_urls=parse_index(index_html)
    for detail_url in detail_urls:
        detail_html=scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s',data)
        logging.info('saving data to json file')
        save_data(data)
        logging.info('data saved successfully')

#使用多进程加速
if __name__ == '__main__':
    pool=multiprocessing.Pool()
    pages=range(1,total_page+1)
    pool.map(main,pages)
    pool.close()
    pool.join()
