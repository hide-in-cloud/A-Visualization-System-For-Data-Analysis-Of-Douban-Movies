import os
import random
import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine
import jieba
from sklearn.metrics.pairwise import pairwise_distances
from functools import reduce
import collections


class RecommendBaseContent:
    """基于内容的推荐"""

    def __init__(self, movie_detail, user_favor, user_rating):
        self.movie_detail = movie_detail
        self.user_favor = user_favor
        self.user_rating = user_rating
        self.user_movie = {}  # 用户电影相关
        self.movie_dataset = self.pickup_tags(movie_detail)
        self.movie_profile = self.create_movie_profile()
        self.inverted_table = self.create_inverted_table()
        self.user_profile = self.create_user_profile()
        self.predict_all_movies = self.predict_all(k=12)

    def pickup_tags(self, movie_detail):
        """挑选出电影标签"""
        # 将每一行类型标签转成列表
        movie_detail['types'] = movie_detail['types'].apply(lambda x: x.split(','))
        # 将每一行导演转成列表
        movie_detail['directors'] = movie_detail['directors'].apply(lambda x: x.split(','))
        # 将每一行演员转成列表
        movie_detail['actors'] = movie_detail['actors'].apply(lambda x: x.split(',') if x is not None else [])
        # 对电影简介用jieba库进行中文分词
        tags = []
        for summary in movie_detail['summary'].values:
            words = list(jieba.cut(summary))
            tags.append(words)
        movie_detail['tags'] = tags
        # 将电影类别和简介合并成标签列
        movie_detail['tags'] = list(map(lambda x,y,z,m: x+y+z+m, movie_detail['types'], movie_detail['tags'], movie_detail['directors'], movie_detail['actors']))
        # 取出其中几列
        columns = ['id', 'title', 'types', 'tags']
        return movie_detail.copy()[columns]

    def create_movie_profile(self):
        """构建电影画像"""
        from gensim.corpora import Dictionary
        from gensim.models import TfidfModel
        dataset = self.movie_dataset['tags'].values
        # 字典对象： key->id(序号)  value->tag标签值
        dct = Dictionary(dataset)
        # [(key,value)] -> [(id, 出现次数)]
        corpus = [dct.doc2bow(line) for line in dataset]
        # 训练TF-IDF模型
        model = TfidfModel(corpus)

        movie_profile = []  # 电影画像
        for i, row in enumerate(self.movie_dataset.itertuples()):
            # 取出每列
            mid = row[1]
            title = row[2]
            types = row[3]
            # 将标签放进TF-IDF训练
            vector = model[corpus[i]]
            # 按照TF-IDF值排序并取出前n个关键词
            movie_tags = sorted(vector, key=lambda x: x[1], reverse=True)[:20]
            # 根据关键词提取对应的电影名称
            tags_weights = dict(map(lambda x: (dct[x[0]], x[1]), movie_tags))
            # 类别词的权重设置为1.0
            for _type in types:
                tags_weights[_type] = 1.0
            # 标签列
            tags = [i[0] for i in tags_weights.items()]
            # 电影画像的每行数据
            movie_profile.append((mid, title, tags, tags_weights))

        df_movie_profile = pd.DataFrame(movie_profile, columns=['id','title','tags','weights'])
        df_movie_profile.set_index('id', inplace=True)
        return df_movie_profile

    def create_inverted_table(self):
        """通过标签找到对应的电影"""
        inverted_table = {}
        for mid, weights in self.movie_profile['weights'].items():
            for tag, weight in weights.items():
                # 用tag作为键去获取值,取不到则返回[]
                value = inverted_table.get(tag, [])
                value.append((mid, weight))
                inverted_table.setdefault(tag, value)
        return inverted_table

    def get_user_interest_words(self, uid, mids):
        """获取用户感兴趣的词以及权重"""
        if not mids:
            return None
        self.user_movie[uid] = mids
        # 取出以上的电影画像
        user_favor_movie = self.movie_profile.loc[mids]
        # 获取这些电影的标签
        user_tags = reduce(lambda x, y: list(x) + list(y), user_favor_movie['tags'].values)
        # 统计每个标签出现的次数
        counter = collections.Counter(user_tags)
        # 取出前40个感兴趣的词
        interest_words = counter.most_common(40)
        # 计算每个词的权重
        maxCount = interest_words[0][1]  # 获取出现最多的次数
        # 权重标准化
        interest_words = [(word, round(count / maxCount, 4)) for word, count in interest_words]
        return interest_words

    def create_user_profile(self):
        """构建用户画像"""
        # 按照用户分组，获取每个用户收藏的电影
        # favor_movie = user_favor.groupby('user_id')['favor_id'].agg(list).to_frame()

        # 获取收藏过或评分过的用户ID
        uids = set(self.user_favor['user_id'].unique()).union(self.user_rating['user_id'].unique())
        # 构建用户画像
        user_profile = {}
        for uid in uids:
            # 用户收藏的电影
            favor_mid = self.user_favor[self.user_favor['user_id'] == uid]['favor_id'].values
            # 用户评分过的电影
            rating_mid = self.user_rating[self.user_rating['user_id'] == uid]['movie_id'].values
            # 合并两个电影id列表
            mids = list(set(favor_mid).union(rating_mid))
            interest_words = self.get_user_interest_words(uid, mids)
            user_profile[uid] = interest_words
        return user_profile

    def update_user_profile(self, uid, mids):
        """更新用户画像"""
        interest_words = self.get_user_interest_words(uid, mids)
        self.user_profile[uid] = interest_words

    def predict_all(self, k):
        """
        预测(推荐)所有用户的电影结果
        :return: 字典类型的 {用户:电影推荐结果}
        """
        predict_all_movies = {}  # {k, v} --> {uid, [mid,mid...]}
        for uid in self.user_profile.keys():
            predict_all_movies[uid] = self.predict_user_movies(uid, k)  # 预测某个用户的电影推荐结果
        return predict_all_movies

    def predict_user_movies(self, uid, k=10):
        """
        预测(推荐)某个用户的电影结果
        :param uid: 用户ID
        :param k: 推荐k部电影
        :return: 推荐电影的ID列表
        """
        # 如果是新用户，则推荐m(k的一半)个热门电影和m(k的一半)个随机电影
        if self.user_profile[uid] is None:
            m = k//2
            # 取近一年的热门电影5个
            df_movie = self.movie_detail.copy()
            df_movie.set_index('id', inplace=True)  # 设置电影id为index
            new_date = df_movie['release_date'].max()  # 最新电影上映日期
            old_date = new_date - pd.Timedelta(360, unit='d')
            recent_df = df_movie[df_movie['release_date'].between(old_date, new_date)]
            # 用评论数来定义热门电影，按评论数来排序，取前50个电影
            top_hot = list(recent_df['comment_len'].sort_values(ascending=False).index[:50])
            top_hot = random.choices(top_hot, k=m)  # 随机取其中的5个电影
            # 取随机电影5个(不包括以上热门电影)
            mids = list(df_movie.index)
            for hot_mid in top_hot:
                mids.remove(hot_mid)
            random_mid = random.choices(mids, k=m)
            # 合并两个ID列表
            return top_hot + random_mid

        # 通过用户感兴趣的标签与电影标签比较，为用户推荐电影
        result_table = {}  # {key,val} --> {mid, 用户感兴趣词在相关电影的权重列表}
        for interest_word, interest_weight in self.user_profile[uid]:
            related_movies = self.inverted_table[interest_word]  # 根据标签反推电影
            for mid, related_weight in related_movies:
                if mid in self.user_movie[uid]:  # 过滤掉已经用户收藏过或评分过的电影
                    continue
                _ = result_table.get(mid, [])

                # _.append(interest_weight)  # 只考虑用户的感兴趣程度
                # _.append(related_weight)  # 只考虑感兴趣词与电影的关联程度
                _.append(interest_weight * related_weight)  # 二者都考虑

                result_table.setdefault(mid, _)
        # 推荐结果
        rs_result = map(lambda x: (x[0], sum(x[1])), result_table.items())  # 将电影的每个权重加起来
        rs_result = sorted(rs_result, key=lambda x: x[1], reverse=True)[:k]  # 按照权重排序，并取前十名
        res_mid = list(map(lambda x: x[0], rs_result))  # 取出其中的电影ID
        return res_mid

    def word2Vec(self):
        """词向量模型，基于文本连续词"""
        from gensim.models.doc2vec import Doc2Vec, TaggedDocument
        movie_tags = self.movie_profile['tags']
        documents = [TaggedDocument(words, [movie_id]) for movie_id, words in movie_tags.items()]
        # 通过向量来表示一篇文档，一篇文档对应一部电影
        # 向量的相似度代表了电影的相似度
        model = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4, epochs=20)
        words = movie_tags.loc[5]
        # print(words)
        inferred_vector = model.infer_vector(words)
        res = model.dv.most_similar(inferred_vector)
        # print(res)
        # print(movie_tags.loc[295])


if __name__ == '__main__':
    # mysql驱动引擎
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
    sql = 'select * from user_favorites;'
    user_favor = pd.read_sql(sql, engine)

    sql = 'select * from movie_detail;'
    movie_detail = pd.read_sql(sql, engine)

    sql = 'select * from user_rating;'
    user_rating = pd.read_sql(sql, engine)

    # 基于内容推荐电影
    a = RecommendBaseContent(movie_detail, user_favor, user_rating)
    print(a.predict_user_movies(4, 12))
    # print(a.word2Vec())
    
    # print(movie_comment['movie_id'].value_counts())
    pass
