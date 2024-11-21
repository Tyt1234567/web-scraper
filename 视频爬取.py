import requests

headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0'}
video = requests.get('https://www.youtube.com/f591ea01-efbd-41f0-a062-3a9c41e23d24',headers=headers).content
print(video)
path = 'cn.mp4'
with open(path, 'wb') as file:
    file.write(video)

