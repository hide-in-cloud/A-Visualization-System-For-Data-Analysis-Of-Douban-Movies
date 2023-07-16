import requests
from faker import Faker
import random
from lxml import etree
import time
import re
import json
import os
import csv
import pymysql
import pandas
from sqlalchemy import create_engine
from spider_ip import ip_to_proxies

# mysql驱动引擎
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
# 爬取时间间隔
DOWNLOAD_DELAY = 5
# User Agent池
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
# Proxies
ip_list = ['166.111.33.72:4780', '1.15.156.141:7890', '8.141.251.188:3128']
proxies_list = ip_to_proxies(ip_list)


def get_first_data(data_list):
    """获取列表的第一个元素"""
    try:
        return data_list[0].strip()
    except:
        # 置为空字符串
        return ""


class Spider(object):
    def __init__(self, file_path='./movies.csv'):
        self.movie_detail = None
        self.file_path = file_path
        self.faker = Faker('zh_CN')
        # self.start = 0  # 从第0条开始读写
        self.total_num = 0
        self.available_num = 0
        self.invalid_num = self.total_num - self.available_num

    def init(self):
        """初始化csv文件"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['title', 'rate', 'detail_url', 'cover', 'year', 'directors', 'actors', 'types',
                                 'countries', 'lang', 'release_date', 'runtime', 'rating_sum', 'stars_proportion',
                                 'summary',
                                 'comment_len', 'comments', 'img_list', 'video'])

    @staticmethod
    def creat_db_table():
        try:
            conn = pymysql.Connect(host='localhost', user='root', password='123456', database='douban_movie', port=3306,
                                   charset='utf8mb4')
            sql = '''
                create table movie_detail(
                    id int primary key auto_increment,
                    title varchar(64) comment '电影名称',
                    rate decimal(2,1) comment '评分',
                    detail_url varchar(255) comment '详情url',
                    cover varchar(255) comment '封面',
                    year varchar(4) comment '年份',
                    directors varchar(255) comment '导演',
                    actors text comment '演员',
                    types varchar(128) comment '类型',
                    countries varchar(128) comment '制片国家',
                    lang varchar(128) comment '语言',
                    release_date varchar(128) comment '上映日期',
                    runtime int comment '片长',
                    rating_sum int comment '星级评分人数',
                    stars_proportion varchar(255) comment '星级评分占比',
                    summary text comment '剧情简介',
                    comment_len int comment '短评人数',
                    img_list text comment '图片列表',
                    video varchar(255) comment '预告片'
                )
            '''
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print('数据库表创建失败:', e)

    @staticmethod
    def creat_db_table_comment():
        try:
            conn = pymysql.Connect(host='localhost', user='root', password='123456', database='douban_movie', port=3306,
                                   charset='utf8mb4')
            sql = '''
                        create table movie_comment(
                            id int primary key auto_increment,
                            user_id int comment '用户ID',
                            movie_id int comment '电影ID',
                            comment_star int comment '星级评分',
                            comment_content text comment '短评内容',
                            comment_time date comment '短评时间'
                        )
                    '''
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print('数据库表创建失败:', e)

    def get_resp(self, url, params=None):
        """发送url请求，获得响应"""
        i = 0
        # 设置三次重连机制
        while i < 3:
            headers = {
                "User-Agent": self.faker.user_agent()
            }
            # proxies = random.choice(proxies_list)
            try:
                resp = requests.get(url=url, params=params, headers=headers)
                if resp.status_code == 200:
                    return resp
                else:
                    print(resp, ':' + url + '不可访问!')
                    # 若url访问异常，则重新访问
                    time.sleep(DOWNLOAD_DELAY)
                    i += 1
            except Exception as e:
                print('url访问异常:', e)
                # 若url访问异常，则重新访问
                time.sleep(DOWNLOAD_DELAY)
                i += 1

    # def spiderHotMovies(self):
    #     # self.file_path = './hot_movies.csv'
    #     self.init()
    #     url = "https://movie.douban.com/j/search_subjects?"
    #     page_limit = 50
    #     page_start = 0
    #     params = {
    #         'type': 'movie',
    #         'tag': '热门',
    #         'page_limit': page_limit,
    #         'page_start': page_start * page_limit
    #     }
    #     proxies = random.choice(proxies_list)
    #     # 网页请求，返回码为200表示成功，json()返回json格式数据
    #     try:
    #         resp_json = requests.get(url, params=params, headers=HEADERS, proxies=proxies).json()
    #         resp_json = resp_json['subjects']
    #     except TimeoutError:
    #         print('请求url超时')
    #         resp_json = []
    #
    #     for index, movieDict in enumerate(resp_json):
    #         print("正在爬取第{}条电影数据".format(index))
    #         movie_data = []
    #         # 电影名字
    #         movie_data.append(movieDict['title'])
    #         # 电影评分
    #         movie_data.append(movieDict['rate'])
    #         # 电影详情地址(detail_url)
    #         movie_data.append(movieDict['url'])
    #         # 电影封面
    #         movie_data.append(movieDict['cover'])
    #         # 详情页面
    #         movie_data = self.get_detailData(movieDict['url'], movie_data)
    #         # 保存到csv文件中，一次写一个电影
    #         self.save_to_csv(movie_data)

    def spiderAllMovies(self, page):
        """爬取所有电影的信息"""
        # file_path = './all_movies.csv'
        self.init()
        # 从第几条数据开始
        start = self.get_movies_sum()
        url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags="

        for i in range(page):
            params = {
                'start': start
            }
            resp = self.get_resp(url, params)
            if resp is None:
                break
            resp_json = resp.json()['data']
            for index, movieDict in enumerate(resp_json):
                print("正在爬取第{}条电影数据".format(start - 1 + index))
                self.total_num += 1
                movie_data = []
                # 电影名字
                movie_data.append(movieDict['title'])
                # 电影评分
                movie_data.append(movieDict['rate'])
                # 电影详情地址(detail_url)
                movie_data.append(movieDict['url'])
                # 电影封面
                movie_data.append(movieDict['cover'])
                # 详情页面
                movie_data = self.get_detailData(movieDict['url'], movie_data)
                # 保存到csv文件中
                self.save_to_csv(movie_data)
                # 等待n秒，防止反爬
                time.sleep(DOWNLOAD_DELAY)
            # 每页20条数据
            start += 20
        print(f'本次爬取到的数据共有:{self.available_num}条')
        print(f'有效数据有:{self.available_num}条')
        print(f'无效数据有:{self.invalid_num}条')

    def get_detailData(self, detail_url, movie_data):
        """爬取详情页面的信息"""
        # 访问详情url
        resp = self.get_resp(detail_url)
        # 若url访问异常，重新访问
        if resp is None:
            self.invalid_num += 1
            print(f'失效数据共有:{self.invalid_num}条')
            return movie_data
        detail_html = etree.HTML(resp.text)  # 解析html网页
        # 电影年份(year)
        year_text = detail_html.xpath('//div[@id="content"]/h1/span[@class="year"]/text()')
        year = get_first_data(year_text)
        year = re.search(r'\d+', year)  # 匹配数字
        if year:
            year = year.group()
        else:
            year = ''
        movie_data.append(year)
        # 电影导演(directors)
        directors = detail_html.xpath('//div[@id="info"]/span[1]/span[2]/a/text()')
        movie_data.append(','.join(directors))
        # 电影演员(actors)
        actors = []
        for ele in detail_html.xpath('//div[@id="info"]/span[3]/span[2]//a'):
            actors.append(ele.text)
        movie_data.append(','.join(actors))
        # 电影类型(types)
        types = []
        for ele in detail_html.xpath('//div[@id="info"]/span[@property="v:genre"]'):
            types.append(ele.text)
        movie_data.append(','.join(types))
        # 电影制片国家(countries)
        countries = detail_html.xpath('//span[.="制片国家/地区:"]/following-sibling::text()[1]')
        countries = get_first_data(countries).split('/')
        countries = ','.join([item.strip() for item in countries])
        movie_data.append(countries)
        # 语言(lang)
        languages = detail_html.xpath('//span[.="语言:"]/following-sibling::text()[1]')
        languages = get_first_data(languages).split('/')
        languages = ','.join([item.strip() for item in languages])
        movie_data.append(languages)
        # 上映日期(release_date)
        release_date = detail_html.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/@content')
        release_date = get_first_data(release_date)
        if len(release_date) >= 7:
            if text := re.search(r"[0-9]{4}-[0-9]{1,2}-[0-3]?[0-9]", release_date):
                release_date = text.group()
            elif text := re.search(r"[0-9]{4}-[0-9]{1,2}", release_date):
                release_date = text.group()
            elif text := re.search(r"[0-9]{4}", release_date):
                release_date = text.group()
            else:
                release_date = ''
        movie_data.append(release_date)
        # 片长(runtime)
        runtime = detail_html.xpath('//div[@id="info"]/span[@property="v:runtime"]/@content')
        runtime = get_first_data(runtime)
        if runtime == '':  # 没有以上对应的标签
            runtime = detail_html.xpath('//div[@id="info"]//span[.="片长:"]/following-sibling::text()[1]')
            runtime = get_first_data(runtime)
        if runtime == '':  # 没有以上对应的标签
            runtime = detail_html.xpath('//div[@id="info"]//span[.="单集片长:"]/following-sibling::text()[1]')
            runtime = get_first_data(runtime)
            runtime = re.search(r'\d+', runtime)
            if runtime:
                runtime = runtime.group()
            else:
                runtime = ''
        # 没有片长则置为空字符串
        movie_data.append(runtime)

        # 星级评分人数(rating_sum)
        rating_sum = detail_html.xpath('//div[@id="interest_sectl"]//div[@class="rating_sum"]/a/span/text()')
        rating_sum = get_first_data(rating_sum)
        movie_data.append(rating_sum)

        # 星级评分占比(stars_proportion)
        # 如果有rating_sum则获取stars_proportion，否则置空
        if rating_sum != '' and int(rating_sum) > 0:
            stars_proportion = []
            items = detail_html.xpath('//div[@id="interest_sectl"]//div[@class="ratings-on-weight"]/div[@class="item"]')
            for ele in items:
                stars_proportion.append(ele.xpath('./span[@class="rating_per"]/text()')[0])
            movie_data.append(','.join(stars_proportion))
        else:
            movie_data.append('')
        # 电影简介(summary)
        summary = detail_html.xpath('//div[@id="link-report-intra"]//span[@property="v:summary"]/text()')
        summary = ''.join([item.strip() for item in summary])
        movie_data.append(summary)
        # 短评条数(comment_len)
        comment_len = detail_html.xpath('//div[@id="comments-section"]/div[1]/h2/span/a/text()')
        comment_len = get_first_data(comment_len)
        comment_len = re.search(r'\d+', comment_len)
        if comment_len:
            comment_len = comment_len.group()
        else:
            comment_len = ''
        movie_data.append(comment_len)
        # 网友短评(comments)
        if comment_len != '' and int(comment_len) > 0:
            comments = []
            for item in detail_html.xpath('//div[@id="hot-comments"]/div[@class="comment-item "]'):
                # 用户名
                user = item.xpath('.//span[@class="comment-info"]/a/text()')[0]
                # 评分星级
                try:
                    comment_star = item.xpath('.//span[@class="comment-info"]/span[2]/@class')[0]
                    comment_star = re.search(r'\d', comment_star).group()
                except:
                    comment_star = '3'
                # 评论时间
                comment_time = item.xpath('.//span[@class="comment-info"]/span[@class="comment-time "]/@title')[0]
                # 评论内容
                if item.xpath('.//p[@class=" comment-content"]/span/@class="full"'):  # 长评论
                    comment_content = item.xpath('.//p[@class=" comment-content"]/span[@class="full"]/text()')[0]
                else:  # 短评论
                    comment_content = item.xpath('.//p[@class=" comment-content"]/span/text()')[0]
                # 用字典格式加入列表中
                comments.append({
                    'user': user,
                    'comment_star': comment_star,
                    'comment_content': comment_content,
                    'comment_time': comment_time,
                })
            movie_data.append(json.dumps(comments))  # 转换成json格式存入

        # 图片列表(img_list)
        img_list = detail_html.xpath('//ul[contains(@class, "related-pic-bd  ")]//img/@src')
        movie_data.append(','.join(img_list))
        # 预告片链接(video)
        video_url = detail_html.xpath('//ul[contains(@class, "related-pic-bd  ")]/li[@class="label-trailer"]/a/@href')
        video_url = get_first_data(video_url)
        if video_url != '':
            resp = self.get_resp(video_url)
            if resp is None:
                movie_data.append('')
            else:
                video_html = etree.HTML(resp.text)
                video = video_html.xpath('//div[@id="movie_player"]//video/source/@src')
                video = get_first_data(video)
                movie_data.append(video)
        else:
            movie_data.append('')

        # 若url访问异常，则重新访问
        if movie_data[4] == '':
            movie_data = movie_data[:4]
            time.sleep(DOWNLOAD_DELAY)
            return self.get_detailData(detail_url, movie_data)
        else:
            self.available_num += 1

        return movie_data

    def get_movies_sum(self):
        return len(open(self.file_path, 'r', encoding='utf-8').readlines()) - 1

    def save_to_csv(self, data):
        """保存到csv文件中，一次写一个电影"""
        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def save_to_sql(self, db_table):
        # if self.start >= self.get_movies_sum():
        #     print('没有新的数据可插入', self.start)
        #     return
        df = pandas.read_csv(self.file_path)  # 读取csv文件
        # 去重
        df.drop_duplicates(subset=['title', 'detail_url'], ignore_index=True, inplace=True)
        # 删除rate为空的数据
        index_list = df.loc[df['rate'].isnull()].index  # 获取rate为空的行标签
        df.drop(index=index_list, inplace=True)
        # 删除真人秀节目
        drop_index = df.loc[df['types'].str.contains('真人秀', na=False)].index
        df.drop(index=drop_index, inplace=True)
        # 设置id
        df.reset_index(drop=True, inplace=True)
        df['id'] = [i + 1 for i in df.index.tolist()]
        df.set_index('id', inplace=True)
        self.movie_detail = df.copy()
        # 删除comments一列
        df.drop(columns='comments', inplace=True)
        # 写到数据库表中(追加的方式)
        df.to_sql(db_table, con=engine, index=False, if_exists='append')

    def save_to_sql_comments(self):
        movie_detail = self.movie_detail.copy()
        # 取出每部电影的短评
        all_comments = movie_detail['comments'].apply(lambda x: json.loads(x))
        rows = []
        for mid, movie_comments in all_comments.items():
            for user_comment in movie_comments:
                username = user_comment.get('user')
                comment_star = user_comment.get('comment_star')
                comment_content = user_comment.get('comment_content')
                comment_time = user_comment.get('comment_time')
                rows.append([username, mid, comment_star, comment_content, comment_time])
        df_comments = pandas.DataFrame(rows,
                                   columns=['username', 'movie_id', 'comment_star', 'comment_content', 'comment_time'])

        # 按照username排序，然后对其编号，同一username为同一编号
        df_comments.sort_values(by='username', inplace=True)
        Number = []
        temp = df_comments['username'].tolist()
        for i, v in enumerate(temp):
            if i == 0:
                Number.append(1)
            elif v == temp[i - 1]:
                Number.append(Number[-1])
            else:
                Number.append(Number[-1] + 1)
        df_comments["username"] = Number
        # 还原顺序
        df_comments.sort_index(inplace=True)
        df_comments['comment_content'] = df_comments['comment_content'].apply(lambda x: json.dumps(x))
        # 写入数据库
        df_comments.to_sql('movie_comment', con=engine, index=False, if_exists='append')


if __name__ == '__main__':
    spider = Spider(file_path='./all_movies2.csv')

    spider.creat_db_table()

    # spider.spiderHotMovies()

    # spider.spiderAllMovies(5)

    spider.save_to_sql('movie_detail')

    spider.save_to_sql_comments()

    pass
