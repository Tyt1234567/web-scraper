from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import sys
import random

#伪装成正常访问，防止学习通检测到爬虫脚本
option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension',False)
login_url='http://passport2.chaoxing.com/login?fid=&newversion=true&refer=http://i.chaoxing.com'
brower=webdriver.Chrome(options = option)
brower.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})

def login(phone_number,password):
    brower.get(login_url)

    phone_text=brower.find_element(By.ID,'phone')
    phone_text.send_keys(phone_number)

    password_text = brower.find_element(By.ID, 'pwd')
    password_text.send_keys(password)

    login_button=brower.find_element(By.ID, 'loginBtn')
    login_button.click()
    time.sleep(2)

def choose_course(course_name):
    #等待页面加载完全并进入课程页面
    try:
        wait=WebDriverWait(brower,10)
        wait.until(EC.presence_of_element_located((By.XPATH,'//a[@name="课程"]')))
    except TimeoutException:
        sys.exit('访问超时,可能由账号密码错误导致，请尝试重新输入')
    else:
        course_botton=brower.find_element(By.XPATH,'//a[@name="课程"]')
        course_botton.click()


    #通过子节点文本（课程名）找到其上三级的节点并进入链接

    try:
        brower.switch_to.frame('frame_content')
        wait=WebDriverWait(brower,10)
        course_title_node=wait.until(EC.presence_of_element_located((By.XPATH,f'//span[@title="{course_name}"]')))
    except TimeoutException:
        sys.exit('未找到该课程，请确认与学习通显示课程名一致')
    else:
        course_node=course_title_node.find_element(By.XPATH,'./ancestor::div')
        course_node=course_node.find_element(By.XPATH,'.//a/img')

        #url链接使用了js加密无法直接获得，所以需要模拟鼠标移动操作
        actions=ActionChains(brower)
        actions.move_to_element(course_node).click().perform()
        #获取当前窗口句柄并切换到新打开页面
        all_window_handles=brower.window_handles
        brower.switch_to.window(all_window_handles[-1])
        time.sleep(2)

#进入章节
def goto_page():
    try:
        wait=WebDriverWait(brower,10)
        wait.until(EC.presence_of_element_located((By.XPATH,'//a[@title="章节"]')))
    except TimeoutException:
        sys.exit('访问超时')
    else:
        course_botton=brower.find_element(By.XPATH,'//a[@title="章节"]')
        course_botton.click()
        time.sleep(2)

#找到所有任务点
def find_all_tasks():
    brower.switch_to.frame('frame_content-zj')
    brower.implicitly_wait(2)
    html=brower.page_source
    soup=BeautifulSoup(html,'lxml')
    tasks=soup.find_all('li')

    return tasks


#筛选未完成的任务点
def find_incomplete_tasks(all_tasks):
    incomplete_tasks=[]
    for task_html in all_tasks:
        soup = BeautifulSoup(str(task_html),'html.parser')
        whether_complete = soup.find('span', class_='bntHoverTips').text
        if whether_complete != "已完成":
            incomplete_tasks.append(task_html)
    return incomplete_tasks

#进入一个未完成的页面，并判断是否有未完成的视频任务点，如果有则播放，没有则返回上一页并删除这个任务
def find_incomplete_tasks_ids(incomplete_tasks):
    #找到未完成的id
    ids=[]
    for incomplete_task in incomplete_tasks:
        soup = BeautifulSoup(str(incomplete_task), 'lxml')
        a = soup.find('div', class_="chapter_item")
        id=a['id']
        ids.append(id)
    return ids

i=1
#通过id进入视频界面并找到所有未观看视频观看
def go_to_video_page(id):
    global i
    go_to_video_botton = brower.find_element(By.ID, id)
    go_to_video_botton.click()
    brower.implicitly_wait(2)
    brower.switch_to.frame('iframe')
    unfinished_video_divs=brower.find_elements(By.XPATH,'//div[@aria-label="任务点未完成"]')
    #通过视频的div节点找到视频同级的iframe
    for unfinished_video_div in unfinished_video_divs:
        unfinished_video_iframe=unfinished_video_div.find_element(By.XPATH,'following-sibling::iframe')
        brower.switch_to.frame(unfinished_video_iframe)
        try:
            wait = WebDriverWait(brower, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="播放视频"]')))
        # 有视频则播放，无视频则返回上级iframe
        except TimeoutException:
            brower.switch_to.frame('iframe')
        else:
            video_element=brower.find_element(By.TAG_NAME,'video')
            brower.execute_script("arguments[0].play();", video_element)
            time.sleep(10)
            while True:
                video_ended=brower.execute_script('return arguments[0].ended;',video_element)
                if video_ended:
                    print(f'本次自动播放完成了第{i}视频')
                    i+=1
                    time.sleep(2)
                    break
                else:
                    sleeptime=random.randint(10,20)
                    print(f'视频播放中,{sleeptime}s后将再次尝试是否播放完成')
                    time.sleep(sleeptime)
            brower.switch_to.parent_frame()


def main():

    course_name = input("请输入课程名：")
    phone_number = input("请输入手机号（学习通账号）：")
    password = input("请输入密码：")
    login(phone_number,password)
    choose_course(course_name)
    goto_page()
    all_tasks=find_all_tasks()
    incomplete_tasks=find_incomplete_tasks(all_tasks)
    incomplete_tasks_ids=find_incomplete_tasks_ids(incomplete_tasks)
    #记录目录页地址
    current_url=brower.current_url
    for id in incomplete_tasks_ids:
        wait = WebDriverWait(brower, 10)
        wait.until(EC.presence_of_element_located((By.ID, id)))
        #观看完成一个页面的视频
        go_to_video_page(str(id))
        #观看完成后返回目录页
        brower.get(current_url)
        #切换iframe
        brower.switch_to.frame('frame_content-zj')


if __name__ == '__main__':
    main()
