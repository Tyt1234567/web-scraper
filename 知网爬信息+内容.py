from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import time
import sys
import pymysql
import mysql.connector
import fitz
import os

KEYWORD = input("请输入您要爬取的关键词:")


# 登录
def login():
    URL = 'https://login.cnki.net/login/?platform=NZKPT&returnUrl=https%3a%2f%2fbar.cnki.net%2fbar%2fdownload%2forder%3fid%3djBGETXBNdPImvx70aLAuJEaV3EyTcVwi28isq7XComhAiTLfM8BW4E%252fPWMov1LwSdIHL2Cy%252blkEQPNV7Ymeogcm82jDOg3yr%252bqRqj9L2CzQX5FOcoxv3%252bj06EVstImPRsJR7S7O3%252bV31gj0tjkn7C2X4FVCnyAFXBdumxVh7%252fso7p0xFNzxqTRsRy65nS12RMczkZWXBbf144Vm1lDbsR%252fiy%252bIPjz%252bULq6HQ8gm4AUc%253d%26source%3d%26isMobile%3dFalse%26returnUrl%3d%26loginNum%3d2%26showpage%3d1&AppendUID=0&ForceReLogin=1&lang=zh-CN'
    response_login = requests.post(URL, json={
        'UserName': '15380982079',
        'Password': 'Tao030506'
    })


MAIN_URL = 'https://www.cnki.net/'
brower = webdriver.Chrome()


def visit_url(url):
    brower.get(url)

    wait = WebDriverWait(brower, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Ecp_top_login"]/a')))
    login_button = brower.find_element(By.XPATH, '//*[@id="Ecp_top_login"]/a')
    login_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Ecp_TextBoxUserName"]')))
    username = brower.find_element(By.XPATH, '// *[ @ id = "Ecp_TextBoxUserName"]')
    username.send_keys('15380982079')
    psw = brower.find_element(By.XPATH, '//*[@id="Ecp_TextBoxPwd"]')
    psw.send_keys('Tao030506')
    time.sleep(3)

    agree = brower.find_element(By.XPATH, '//*[@id="agreement"]')
    agree.click()


    confirm = brower.find_element(By.XPATH, '//*[@id="Ecp_Button1"]')
    confirm.click()
    time.sleep(3)




# 搜索关键词
def search_keyword(keyword):
    input = brower.find_element(By.ID, 'txt_SearchText')
    input.send_keys(keyword)
    input.send_keys(Keys.RETURN)


# 获取任意目录页HTML
def get_main_html():
    try:
        wait = WebDriverWait(brower, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="fz14"]')))
    except TimeoutException:
        sys.exit('访问超时')
    else:
        main_html = brower.page_source
        return main_html


# 获取总页数
def get_total_page_number(main_html):
    soup = BeautifulSoup(main_html, 'lxml')
    page_number = soup.find('span', class_='countPageMark')
    return int(page_number['data-pagenum'])


# 找到该目录页所有标题
def find_titles(html):
    soup = BeautifulSoup(html, 'lxml')
    target_tags = soup.find_all('a', class_='fz14')
    titles = []
    for target_tag in target_tags:
        title = ''.join(target_tag.stripped_strings)
        titles.append(title)
    return titles


# 找到该目录页所有文章作者
def find_authors(html):
    soup = BeautifulSoup(html, 'lxml')
    target_tags = soup.find_all('td', class_='author')

    authors = []
    for target_tag in target_tags:
        target_tags2 = target_tag.find_all('a', class_='KnowledgeNetLink')
        names = []
        for name in target_tags2:
            names.append(name.text)
        authors.append(names)
    return authors


# 找到该目录页所有期刊来源
def find_sources(html):
    soup = BeautifulSoup(html, 'lxml')
    target_tags = soup.find_all('td', class_='source')

    sources = []
    for target_tag in target_tags:
        source = target_tag.find('a')
        sources.append(source.text)
    return sources


# 找到该目录页所有发表日期
def find_dates(html):
    soup = BeautifulSoup(html, 'lxml')
    target_tags = soup.find_all('td', class_='date')

    dates = []
    for target_tag in target_tags:
        dates.append(target_tag.text)
    return dates


# 找到该目录页所有数据库来源
def find_dbs(html):
    soup = BeautifulSoup(html, 'lxml')
    target_tags = soup.find_all('td', class_='data')

    dbs = []
    for target_tag in target_tags:
        data = target_tag.find('span')
        dbs.append(data.text)
    return dbs


def find_essay_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    target_tags = soup.find_all('a', class_='fz14')

    essay_urls = []
    for target_tag in target_tags:
        essay_url = target_tag.get('href')
        essay_urls.append(essay_url)
    return essay_urls

#下载论文
def download_essay_context(essay_url):
    browerdl=webdriver.Chrome()
    browerdl.get(essay_url)
    try:
        waitdl=WebDriverWait(browerdl,100)
        waitdl.until(EC.presence_of_element_located((By.ID,'pdfDown')))
    except TimeoutException:
        print('下载超时')
        return
    else:
        button=browerdl.find_element(By.ID,'pdfDown')
        button.click()
        time.sleep(3)

#下面开始获得pdf内容，读取一个删除一个（保证文件只有一个）
folder_path=r'C:\Users\yutiantao\Downloads'

#获取pdf路径
def find_path():
    for file in os.scandir(folder_path):
        if file.is_file() and file.path.lower().endswith(('.pdf')):
            return file.path
        if len(os.listdir(folder_path))==1:
            time.sleep(2)
            return None

#获取pdf内容
def read_pdf_context(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text += page.get_text()
    pdf_document.close()
    text = text.replace("\n", "")
    return text

#删除pdf
def del_file(file_path):
    os.remove(file_path)


# 检查数据库中是否已经存在该表，若存在则退出
def check_table_unexisted(table_name):
    # 连接到MySQL数据库
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='知网', charset='utf8')
    # 创建游标对象
    cursor = conn.cursor()
    # 执行查询是否存在表的SQL语句
    check_table_query = f'''
    SELECT TABLE_NAME
    FROM information_schema.tables
    WHERE TABLE_SCHEMA = '{conn.database}'
      AND TABLE_NAME = '{table_name}';
    '''
    cursor.execute(check_table_query)
    # 获取查询结果
    result = cursor.fetchone()
    # 判断是否存在表
    if result:
        sys.exit(f"表 '{table_name}' 存在于数据库中。")
    # 关闭连接
    conn.close()


# 若不存在则创建
def create_mysql_table(table_name):
    con = pymysql.connect(host='localhost', user='root', password='', database='知网', charset='utf8')
    cursor = con.cursor()
    sql = f'CREATE TABLE IF NOT EXISTS {table_name} (标题 TEXT,作者 TEXT,来源 TEXT,发表时间 TEXT,数据库 TEXT,链接 TEXT,内容 TEXT)'
    cursor.execute(sql)
    con.close()


# 存储至mysql数据库
con = pymysql.connect(host='localhost', user='root', password='', database='知网', charset='utf8')
sql = f"INSERT INTO {KEYWORD}(标题,作者,来源,发表时间,数据库,链接,内容) VALUES(%s,%s,%s,%s,%s,%s,%s)"
cursor = con.cursor()


def save_data(data):  # data
    val = data
    cursor.execute(sql, val)
    con.commit()


# 程序执行
def main():
    # 登录
    login()
    # 打开知网
    visit_url(MAIN_URL)
    # 输入关键词
    search_keyword(KEYWORD)
    # 获得HTML源代码，找到搜索的总页数
    main_html = get_main_html()
    total_page_number = get_total_page_number(main_html)
    # 检查是否已经存在该表，有则退出没有则创建
    check_table_unexisted(KEYWORD)
    create_mysql_table(KEYWORD)

    for _ in range(total_page_number - 1):

        # 获取当前页面中所有论文地址
        titles = find_titles(main_html)
        authors = find_authors(main_html)
        sources = find_sources(main_html)
        dates = find_dates(main_html)
        dbs = find_dbs(main_html)
        essay_urls = find_essay_urls(main_html)

        i = 0
        for k in range(len(titles)):
            title = titles[i]
            author = ','.join(authors[i])
            source = sources[i]
            date = dates[i]
            db = dbs[i]
            url = essay_urls[i]

            # 下载
            download_essay_context(url)
            # 等待文件下载完成并获取路径
            while find_path() == None:
                find_path()
            file_path = find_path()
            # 读取文本
            essay_context = read_pdf_context(file_path)
            # 删除
            del_file(file_path)

            save_data([title, author, source, date, db, url, essay_context])
            print(f'{title}存入成功')
            i += 1

        # 翻页
        next_page_button = brower.find_element(By.ID, 'PageNext')
        next_page_button.click()
        # 等待新的一页html加载完全
        brower.implicitly_wait(2)
        time.sleep(2)
        # 获取新的一页html代码
        main_html = get_main_html()
    brower.close()


if __name__ == '__main__':
    main()



