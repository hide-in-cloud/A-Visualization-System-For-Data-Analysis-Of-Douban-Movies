import os
import pandas as pd
from sqlalchemy import create_engine

CACHE_DIR = './cache'
rating_matrix_cache = 'rating_matrix.cache'
user_similarity_cache = 'user_similarity.cache'


def get_rating_matrix(user_rating):
    """获取用户对电影的评分矩阵"""
    rating_matrix_path = os.path.join(CACHE_DIR, rating_matrix_cache)
    if os.path.exists(rating_matrix_path):
        print('从缓存中加载用户对物品评分矩阵')
        rating_matrix = pd.read_pickle(rating_matrix_path)
    else:
        rating_matrix = pd.pivot_table(user_rating, index=['user_id'], columns=['movie_id'], values='star_rating')
        # print(rating_matrix)
        # rating_matrix.to_pickle(rating_matrix_path)
    return rating_matrix


def compute_pearson_similarity(rating_matrix):
    """计算皮尔逊相关系数，得到相似用户矩阵"""
    user_similarity_cache_path = os.path.join(CACHE_DIR, user_similarity_cache)
    if os.path.exists(user_similarity_cache_path):
        pearson_similarity = pd.read_pickle(user_similarity_cache_path)
    else:
        pearson_similarity = rating_matrix.T.corr(method='pearson', min_periods=1)
        # print(pearson_similarity)
        # pearson_similarity.to_pickle(user_similarity_cache_path)
    return pearson_similarity


def predict_base_pearson(uid, mid, rating_matrix, user_similarity):
    """
    预测给定用户对给定电影的评分值
    :param uid:用户ID
    :param mid:电影ID
    :param rating_matrix:评分矩阵
    :param user_similarity:用户相似矩阵
    :return:预测的评分值
    """
    # 1.找出uid用户的相似用户
    if uid not in user_similarity:
        print('没有用户行为数据')
    similar_users = user_similarity[uid].drop([uid]).dropna()  # 去除自己的数据和空的数据
    # 相似用户筛选规则：正相关的用户(相关系数>0)
    similar_users = similar_users.where(similar_users > 0).dropna()
    if similar_users.empty:
        raise Exception(f'用户{uid}没有相似的用户')
    # 2. 从uid用户的近邻相似用户中筛选出对mid电影有过评分的近邻用户
    ids = set(rating_matrix[mid].dropna().index) & set(similar_users.index)
    finally_similar_users = similar_users.loc[list(ids)]
    # print('相似用户:', finally_similar_users)
    # 3. 结合mid物品与其相似物品的相似度和uid用户对其相似物品的评分，预测uid对mid的评分
    sum_up = 0  # 评分预测公式的分子部分
    sum_down = 0  # 评分预测公式的分母部分
    for sim_uid, similarity in finally_similar_users.items():
        # 近邻用户的评分数据
        sim_user_rated_movies = rating_matrix.loc[sim_uid].dropna()
        # 近邻用户对mid物品的评分
        sim_user_rating_for_mid = sim_user_rated_movies[mid]
        # 分子
        sum_up += similarity * sim_user_rating_for_mid
        # 分母
        sum_down += similarity
    # 计算预测的评分值并返回
    predict_rating = sum_up / sum_down
    # print(predict_rating)
    return round(predict_rating, 2)


def predict_all_base_pearson(uid, rating_matrix, user_similar):
    """
    预测指定用户的全部电影的评分
    :param uid:用户ID
    :param rating_matrix:评分矩阵
    :param user_similar:用户相似矩阵
    :return:
    """
    # 当前用户没有评过分
    if uid not in rating_matrix.index:
        print('没有用户行为数据')
        return []
    user_ratings = rating_matrix.loc[uid]
    _ = user_ratings < 6
    movie_ids = _.where(_ == False).dropna().index
    for mid in movie_ids:
        try:
            rating = predict_base_pearson(uid, mid, rating_matrix, user_similar)
        except Exception as e:
            print(e)
            break
        else:
            yield uid, mid, rating


# ############    余弦相似度     ###############


def compute_cos_sim(user_id, rating_matrix):
    """计算余弦相似度"""
    import numpy as np
    similarity = {}
    # 目标用户向量
    vec1 = np.array(rating_matrix.loc[user_id])
    vec1 = np.nan_to_num(vec1)
    # 遍历其余用户，计算他们的余弦相似度
    for i in rating_matrix.index:
        if i == user_id:
            continue
        # 用户向量2
        vec2 = np.array(rating_matrix.loc[i])
        vec2 = np.nan_to_num(vec2)
        # 余弦相似度：两向量点乘/两向量的模的乘积
        cos_sim = vec1.dot(vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        similarity[i] = cos_sim
    # 选取相似度大于0的用户
    user_similarity = dict(filter(lambda x: x[1] > 0, similarity.items()))
    # 选取最相似的前5名用户
    cos_similar_users = dict(sorted(user_similarity.items(), key=lambda x: x[1], reverse=True)[:5])
    # print(cos_similar_users)
    return cos_similar_users


def predict_base_cos(mid, rating_matrix, user_similarity):
    """
    基于余弦相似度预测电影评分
    :param mid:
    :param rating_matrix:
    :param user_similarity:
    :return:
    """
    sum_up = 0  # 评分预测公式的分子部分
    sum_down = 0  # 评分预测公式的分母部分
    for sim_uid, similarity in user_similarity.items():
        # 近邻用户的评分数据
        sim_user_rated_movies = rating_matrix.loc[sim_uid].dropna()
        if mid in sim_user_rated_movies:
            # 近邻用户对mid物品的评分
            sim_user_rating_for_mid = sim_user_rated_movies[mid]
        else:
            sim_user_rating_for_mid = 0
        # 分子
        sum_up += similarity * sim_user_rating_for_mid
        # 分母
        sum_down += similarity
    # 计算预测的评分值并返回
    predict_rating = sum_up / sum_down
    # print('predict_rating=',predict_rating)
    return round(predict_rating, 2)


def predict_all_base_cos(uid, rating_matrix, user_similar):
    """
    预测指定用户的全部电影的评分
    :param uid:用户ID
    :param rating_matrix:评分矩阵
    :param user_similar:用户相似矩阵
    :return:
    """
    # 当前用户没有评过分
    if uid not in rating_matrix.index:
        print('没有用户行为数据')
        return []
    user_ratings = rating_matrix.loc[uid]
    _ = user_ratings < 6
    movie_ids = _.where(_ == False).dropna().index
    for mid in movie_ids:
        try:
            rating = predict_base_cos(mid, rating_matrix, user_similar)
        except Exception as e:
            print(e)
            break
        else:
            yield uid, mid, rating


def top_k_rs_mid(results, k):
    """按照预测的评分排序，取前k个预测结果的mid"""
    top_results = sorted(results, key=lambda x: x[2], reverse=True)[:k]
    return list(map(lambda x: x[1], top_results))


def user_based_CF(user_rating, uid, k):
    """基于用户的协同过滤推荐"""
    # 基于皮尔逊相关系数计算用户相似度
    rating_matrix = get_rating_matrix(user_rating)
    pearson_similarity = compute_pearson_similarity(rating_matrix)
    results = predict_all_base_pearson(uid, rating_matrix, pearson_similarity)
    mids = top_k_rs_mid(results, k)
    # 若皮尔逊相关系数没有相似用户(矩阵是稀疏的)，则使用余弦相似度来计算用户相似度
    # if not mids:
    #     cos_similarity = compute_cos_sim(uid, rating_matrix)
    #     results = predict_all_base_cos(uid, rating_matrix, cos_similarity)
    #     mids = top_k_rs_mid(results, k)
    return mids


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
    sql = 'select * from user_rating;'
    user_rating = pd.read_sql(sql, engine)
    # 基于user-CF推荐电影
    print(user_based_CF(user_rating, 2, 12))
