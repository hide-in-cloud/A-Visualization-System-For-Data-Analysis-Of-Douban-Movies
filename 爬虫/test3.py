import spider
import requests
from lxml import etree
import re


def get_first_data(data_list):
    try:
        return data_list[0].strip()
    except:
        return ""

# mySpider = spider.Spider()
data = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
# 详情页面
detail_html = requests.get('https://movie.douban.com/subject/1303037/', headers=headers).text
detail_html = etree.HTML(detail_html)  # 解析html网页

release_date = detail_html.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/@content')
release_date = get_first_data(release_date)
if len(release_date) >= 7:
    if text := re.search(r"[0-9]{4}-[0-9]{1,2}-[0-3]?[0-9]", release_date):
        release_date = text.group()
        print(release_date)
    elif text := re.search(r"[0-9]{4}-[0-9]{1,2}", release_date):
        release_date = text.group()
        print(release_date)
    elif text := re.search(r"[0-9]{4}", release_date):
        release_date = text.group()
        print(release_date)
    else:
        release_date = ''

