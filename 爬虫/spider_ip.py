import requests  # 导入模块
from lxml import etree
from faker import Faker


# 简单的反爬，设置一个请求头来伪装成浏览器
def request_header():
    f = Faker('zh_CN')
    headers = {
        'User-Agent': f.user_agent()  # 谷歌浏览器
    }
    return headers


'''
创建两个列表用来存放代理ip
'''
all_ip_list = []  # 用于存放从网站上抓取到的ip
usable_ip_list = []  # 用于存放通过检测ip后是否可以使用


# 发送请求，获得响应
def get_ip_list():
    # 爬取5页，可自行修改
    for i in range(1, 6):
        print(f'正在抓取第{i}页……')
        response = requests.get(url=f'http://www.ip3366.net/free/?page={i}', headers=request_header())
        text = response.text.encode('ISO-8859-1')
        # print(text.decode('gbk'))
        # 使用xpath解析，提取出数据ip，端口
        html = etree.HTML(text)
        tr_list = html.xpath('/html/body/div[2]/div/div[2]/table/tbody/tr')
        for td in tr_list:
            ip_ = td.xpath('./td[1]/text()')[0]  # ip
            port_ = td.xpath('./td[2]/text()')[0]  # 端口
            proxy = ip_ + ':' + port_  # 115.218.5.5:9000
            all_ip_list.append(proxy)
            test_ip(proxy)  # 开始检测获取到的ip是否可以使用
    print('抓取完成！')
    print(f'抓取到的ip个数为：{len(all_ip_list)}')
    print(f'可以使用的ip个数为：{len(usable_ip_list)}')
    print('分别有：\n', usable_ip_list)
    return usable_ip_list


# 检测ip是否可以使用
def test_ip(proxy):
    # 构建代理ip
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy
    }
    try:
        response = requests.get(url='https://www.baidu.com/', headers=request_header(), proxies=proxies,
                                timeout=1)  # 设置timeout，使响应等待1s
        response.close()
        if response.status_code == 200:
            usable_ip_list.append(proxy)
            print(proxy, '\033[31m可用\033[0m')
        else:
            print(proxy, '不可用')
    except:
        print(proxy, '请求异常')


def ip_to_proxies(ip_list):
    proxies_list = []
    for ip in ip_list:
        proxy = {
            "http": "http://" + ip,
            "https": "http://" + ip
        }
        proxies_list.append(proxy)
    return proxies_list


if __name__ == '__main__':
    ip_to_proxies(get_ip_list())
