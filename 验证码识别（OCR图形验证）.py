import time
import re
import pytesseract
from PIL import Image
import numpy as np
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

#对图片进行去噪处理
def preprocess(image):
    image = image.convert('L') #转为灰度图
    array = np.array(image)
    threshold = 120
    array = np.where(array > threshold, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image

def login():
    brower = webdriver.Chrome()
    brower.get('https://captcha7.scrape.center')
    username = brower.find_element(By.CSS_SELECTOR, '.username input[type="text"]')
    username.send_keys('admin')
    password = brower.find_element(By.CSS_SELECTOR, '.password input[type="password"]')
    password.send_keys('admin')

    captcha = brower.find_element(By.CSS_SELECTOR, '#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    image = preprocess(image)
    captcha = pytesseract.image_to_string(image)
    captcha = re.sub('[^A-Za-z0-9]','',captcha)
    brower.find_element(By.CSS_SELECTOR,'.captcha input[type="text"]').send_keys(captcha)
    brower.find_element(By.CSS_SELECTOR,'.login').click()
    try:
        WebDriverWait(brower,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div/div/div/h2')))
        print('验证码识别正确，登录成功')
        time.sleep(10)
        return True
    except TimeoutException:
        print('验证码识别错误')
        return False

if __name__ == '__main__':
    while True:
        login()
        if login() == False:
            login()
        else:
            break