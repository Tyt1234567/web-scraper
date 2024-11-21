import asyncio
import aiohttp
from tqdm import tqdm


async def get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    session=aiohttp.ClientSession()
    response=await session.get(url,headers=headers)
    await response.text()
    await session.close()
    return response

async def request():
    url = 'https://www.cugb.edu.cn'
    print('waiting for', url)
    response= await get(url)
    print('get response from',url,'response',response)

tasks=[asyncio.ensure_future(request()) for _ in tqdm(range(10))]
loop=asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

