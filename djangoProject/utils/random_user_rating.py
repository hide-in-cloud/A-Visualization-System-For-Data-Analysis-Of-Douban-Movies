import random
from datetime import datetime
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# mysql驱动引擎
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
sql = 'select * from movie_detail;'
movie_detail = pd.read_sql(sql, engine)
sql = 'select * from movie_comment;'
movie_comment = pd.read_sql(sql, engine)
sql = 'select * from user_rating;'
user_rating = pd.read_sql(sql, engine)


def test(uid, k):
    """随机评分"""
    conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='douban_movie',
                           charset='utf8')
    cur = conn.cursor()
    try:
        # 查询表中是否存在该用户
        sql_word = "SELECT * FROM user_info WHERE id=%s;"
        cur.execute(sql_word, uid)
        user_exist = cur.fetchone()
        if user_exist is None:
            raise Exception(f"当前用户{uid}未注册")
        else:
            # 查询表中是否存在该用户的数据
            sql_word = "SELECT * FROM user_rating WHERE user_id=%s;"
            cur.execute(sql_word, uid)
            data_exist = cur.fetchone()
            if data_exist is not None:
                raise Exception(f"当前用户{uid}在表'user_rating'已存在数据")
            else:
                # 插入数据
                sql_word = "INSERT INTO user_rating(user_id,movie_id,star_rating,create_time) VALUES(%s,%s,%s,%s);"
                mids = movie_detail['id'].values.tolist()
                # 随机对k部进行电影
                for mid in random.choices(mids, k=k):
                    try:
                        cur.execute(sql_word, (uid, mid, random.randint(1, 5), datetime.now()))
                        conn.commit()
                    except Exception as e:
                        print('插入失败:', e)
                        conn.rollback()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def test2():
    df = movie_comment.sort_values('username')
    df.drop(columns='comment_content', inplace=True)
    df.columns = ['user_id', 'movie_id', 'star_rating', 'create_time']
    user_ids = df['user_id'].value_counts()[:10]
    print(user_ids.index)
    df = df[df['user_id'] == 2289]
    df['user_id'] = [22] * df.shape[0]
    print(df)
    df.to_sql('user_rating', engine, index=False, if_exists='append')


def test3(user_id):
    """从movie_comment表中统计评分"""
    from scipy import stats

    conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='douban_movie',
                           charset='utf8')
    cur = conn.cursor()
    sql_word = "SELECT * FROM user_rating WHERE user_id=%s;"
    try:
        cur.execute(sql_word, user_id)
        user_exist = cur.fetchone()
        # 查询表中是否存在该用户的数据
        if user_exist is not None:
            raise Exception(f"当前用户{user_id}在表'user_rating'已存在数据")
        else:
            df = movie_comment[['movie_id', 'comment_star']]
            # df = df.groupby(['movie_id']).median()  # 取评分的中位数
            # df = df.groupby(['movie_id']).max()  # 取评分的最大值
            # df = df.groupby(['movie_id']).min()  # 取评分的最小值
            # df = df.groupby(['movie_id']).agg(lambda x:x.value_counts().index[0])  # 取评分的众数中较大的结果
            df = df.groupby(['movie_id']).agg(lambda x:stats.mode(x)[0][0])  # 取评分的众数中较小的结果
            df.rename(columns={'comment_star': 'star_rating'}, inplace=True)  # 修改列名，与数据库对应
            df['user_id'] = [user_id] * len(df)
            df['create_time'] = [datetime.now()] * len(df)
            print(df)
            # 写入数据库
            df.to_sql('user_rating', engine, index=True, if_exists='append')
    except Exception as e:
        print(e)
        conn.rollback()
    cur.close()
    conn.close()


if __name__ == '__main__':
    test(uid=35, k=12)
    # test3(29)
