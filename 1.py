import requests
import bs4

response = requests.get('http://eol.yzu.edu.cn/meol/styles/newstyle/plugins/DPFjsc/web/viewer.html;jsessionid=177D1CB5D760333EDA2C7A2C86709620?file=%2Fmeol%2Fanalytics%2FresPdfShow.do%3Bjsessionid%3D177D1CB5D760333EDA2C7A2C86709620%3FresId%3D813230%26lid%3D95391&lid=95391&resId=813230')

soup = bs4.BeautifulSoup(response.content,'html.parser')

# 找到iframe标签并获取其src属性值
iframe_src = soup.find("iframe")["src"]

# 访问iframe中的页面并解析
iframe_response = requests.get(iframe_src)
soup = bs4.BeautifulSoup(iframe_response.content, "html.parser")



spans = soup.find_all('span')
for span in spans:
    print(span.text)