import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
import requests


KEYWORD='造山型金矿'
width,height = 1366, 768
#登录
def login():
    URL = 'https://login.cnki.net/login/?platform=NZKPT&returnUrl=https%3a%2f%2fbar.cnki.net%2fbar%2fdownload%2forder%3fid%3djBGETXBNdPImvx70aLAuJEaV3EyTcVwi28isq7XComjfol9VFY7iY%252fM0grhSnMC3k3PgOdB%252f8KZdF0hYj%252bY0tESjJNzYPfoYyyFikZw3RsIr4qya3J1MXVAeiRx5OlqsTexkrKzFwIrft71n9EQs%252fUN1tZaOZ9Yf2CwqWvTYvKuGHjw26TQ0hXDvTs5DiLWgkrETngyBnCTl55KHYlBwNAXrVaaUzgl9XV67BcERvso%253d%26source%3d%26isMobile%3dFalse%26returnUrl%3d%26loginNum%3d2%26showpage%3d1&AppendUID=0&ForceReLogin=1&lang=zh-CN'
    requests.post(URL, json={
        'UserName': '15380982079',
        'Password': 'Tao030506'
    })

MAIN_URL='https://www.cnki.net/'
async def main():
    login()
    brower = await launch(headless=False, devtools=False, args=['--disable-infobars', f'--window-size={width},{height}'],userDataDir='./userdata')
    context = await brower.createIncognitoBrowserContext() #开启无痕模式
    page=await context.newPage()
    await page.evaluateOnNewDocument(
        'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})')  # 防止识别到Webdriver
    await page.setViewport({'width': width, 'height': height})  # 设置页面大小
    await page.goto('https://www.cnki.net/')
    await page.waitForSelector('#txt_SearchText')
    await page.type('#txt_SearchText', '造山型金矿')
    await page.click('.search-btn', options={'button': 'left', 'clickCount': 1, 'delay': 300})
    await page.waitForNavigation()
    print(await page.content())
    print(await page.cookies())
    await asyncio.sleep(100)
    await brower.close()

asyncio.get_event_loop().run_until_complete(main())

