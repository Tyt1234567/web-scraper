from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


#初始浏览器对象
brower=webdriver.Chrome()

#访问页面
brower.get('https://www.taobao.com')

#输入

input=brower.find_element(By.XPATH,'//input')
input.send_keys('习近平谈治国理政')

#模拟点击
#button=brower.find_element(By.XPATH,'//button')
#button.click()
#输入回车
from selenium.webdriver.common.keys import Keys
input.send_keys(Keys.RETURN)


time.sleep(100)
#关闭浏览器
brower.close()


"""
#拖动
url='https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
brower.get(url)
brower.switch_to.frame('iframeResult')

source=brower.find_element(By.CSS_SELECTOR,'#draggable')
target=brower.find_element(By.CSS_SELECTOR,'#droppable')

actions=ActionChains(brower)
actions.drag_and_drop(source,target)
actions.perform()
"""