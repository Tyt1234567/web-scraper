from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import requests
import time
import fitz
import os
import pymongo


MAIN_URL='https://www.cnki.net/'
brower=webdriver.Chrome()
def visit_url(url):
    brower.get(url)

#搜索关键词
def search_keyword(keyword):
    input=brower.find_element(By.ID,'txt_SearchText')
    input.send_keys(keyword)
    input.send_keys(Keys.RETURN)

#获取目录页HTML
def get_main_html():
    wait=WebDriverWait(brower,10)
    wait.until(EC.presence_of_element_located((By.XPATH,'//a[@class="fz14"]')))
    main_html = brower.page_source
    return main_html

#获取总页数
def get_total_page_number(main_html):
    soup = BeautifulSoup(main_html, 'lxml')
    page_number=soup.find('span',class_='countPageMark')
    return int(page_number['data-pagenum'])

#获取当前目录页的所有论文地址
def get_essay_url(main_html):
    soup=BeautifulSoup(main_html,'lxml')
    urls=soup.find_all('a',class_='fz14')
    essay_urls=[]
    for url in urls:
        essay_urls.append(url['href'])
    return essay_urls

#下载论文
def download_essay_context(essay_url):
    browerdl=webdriver.Chrome()
    browerdl.get(essay_url)
    waitdl=WebDriverWait(browerdl,10)
    waitdl.until(EC.presence_of_element_located((By.ID,'pdfDown')))
    button=browerdl.find_element(By.ID,'pdfDown')
    button.click()

    if 'login' in str(browerdl.current_url):
        login()
    time.sleep(3)

#登录
def login():
    #打开并等待页面
    browerlogin = webdriver.Chrome()
    browerlogin.get('https://login.cnki.net/login/?platform=NZKPT&returnUrl=https%3a%2f%2fbar.cnki.net%2fbar%2fdownload%2forder%3fid%3djBGETXBNdPImvx70aLAuJEaV3EyTcVwi28isq7XComjfol9VFY7iY%252fM0grhSnMC3k3PgOdB%252f8KZdF0hYj%252bY0tESjJNzYPfoYyyFikZw3RsIr4qya3J1MXVAeiRx5OlqsTexkrKzFwIrft71n9EQs%252fUN1tZaOZ9Yf2CwqWvTYvKuGHjw26TQ0hXDvTs5DiLWgkrETngyBnCTl55KHYlBwNAXrVaaUzgl9XV67BcERvso%253d%26source%3d%26isMobile%3dFalse%26returnUrl%3d%26loginNum%3d2%26showpage%3d1&AppendUID=0&ForceReLogin=1&lang=zh-CN')

    waitlogin = WebDriverWait(browerlogin, 10)
    waitlogin.until(EC.presence_of_element_located((By.ID, "TextBoxUserName")))

    #用户名
    inputname = browerlogin.find_element(By.ID, "TextBoxUserName")
    inputname.send_keys('15380982079')
    #密码
    inputpw = browerlogin.find_element(By.ID, "TextBoxPwd")
    inputpw.send_keys('Tao030506')

    #点击登录按钮
    buttonlogin = browerlogin.find_element(By.ID, 'Button1')
    buttonlogin.click()
    time.sleep(1)

    browerlogin.close()



#下面开始获得pdf内容，读取一个删除一个（保证文件只有一个）
folder_path=r'C:\Users\yyuti\Downloads'

#获取pdf路径
def find_path():
    for file in os.listdir(folder_path):
        file_path=os.path.join(folder_path,file)
        if os.path.isfile(file_path) and file.lower().endswith(('.pdf')):
            return file_path
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



#程序执行
def main():
    visit_url(MAIN_URL)
    search_keyword('造山型金矿')
    main_html=get_main_html()
    essay_urls=get_essay_url(main_html)
    total_page_number=get_total_page_number(main_html)
    for _ in range(total_page_number-1):
        for essay_url in essay_urls:
            download_essay_context(essay_url)
            #file_path=find_path()
            #essay_context=read_pdf_context(file_path)
            #del_file(file_path)

        next_page_button = brower.find_element(By.ID, 'PageNext')
        next_page_button.click()

    time.sleep(5)
    brower.close()

if __name__ == '__main__':
    main()
