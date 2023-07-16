import math
import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import pairwise_distances

CACHE_DIR = './cache'
data_path = 'data.csv'
item_similar_cache_path = 'item_similar.csv'
rating_matrix_cache = 'rating_matrix.cache'
user_similarity_cache = 'user_similarity.cache'


def get_rating_matrix(user_rating):
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
    """计算皮尔逊相关系数，得到相似物品矩阵"""
    user_similarity_cache_path = os.path.join(CACHE_DIR, user_similarity_cache)
    if os.path.exists(user_similarity_cache_path):
        pearson_similarity = pd.read_pickle(user_similarity_cache_path)
    else:
        pearson_similarity = rating_matrix.corr(method='pearson', min_periods=1)
        # print(pearson_similarity)
        # pearson_similarity.to_pickle(user_similarity_cache_path)
    return pearson_similarity


def predict_base_pearson(uid, mid, rating_matrix, item_similarity):
    """
    预测给定用户对给定电影的评分值:
    根据当前用户对当前电影的相似电影的评分去预测电影评分
    :param uid:用户ID
    :param mid:电影ID
    :param rating_matrix:评分矩阵
    :param item_similarity:物品相似矩阵
    :return: 预测的评分值
    """
    # 1.找出mid物品的相似物品
    similar_items = item_similarity[mid].drop([mid]).dropna()  # 去除自己的数据和空的数据
    # 相似物品筛选规则：正相关的物品(相关系数>0)
    similar_items = similar_items.where(similar_items > 0).dropna()
    if similar_items.empty:
        raise Exception(f'物品{mid}没有相似的物品')

    # 2. 从mid物品的近邻相似物品中筛选出uid用户评分过的物品
    ids = set(rating_matrix[uid].dropna().index) & set(similar_items.index)
    finally_similar_items = similar_items.loc[list(ids)]

    # 3. 结合mid物品与其相似物品的相似度和uid用户对其相似物品的评分，预测uid对mid的评分
    sum_up = 0  # 评分预测公式的分子部分
    sum_down = 0  # 评分预测公式的分母部分
    for sim_mid, similarity in finally_similar_items.items():
        # 近邻物品的评分数据
        sim_item_rated_movies = rating_matrix.loc[sim_mid].dropna()
        # uid用户对相似物品的评分
        sim_item_rating_for_mid = sim_item_rated_movies[uid]
        # 分子
        sum_up += similarity * sim_item_rating_for_mid
        # 分母
        sum_down += similarity
    # 计算预测的评分值并返回
    predict_rating = sum_up / sum_down
    # print('预测:',uid, mid, predict_rating)
    return round(predict_rating, 2)


def predict_all_base_pearson(uid, rating_matrix, item_similarity):
    """
    预测指定用户的全部电影的评分
    :param uid:用户ID
    :param rating_matrix:评分矩阵
    :param item_similarity:物品相似矩阵
    :return:
    """
    # 当前用户没有评过分
    if uid not in rating_matrix.index:
        print('没有用户行为数据')
        return []
    user_ratings = rating_matrix.loc[uid]
    _ = user_ratings < 6
    # 过滤掉用户已评过分的物品
    movie_ids = _.where(_ == False).dropna().index
    # 遍历剩余的电影，预测其评分
    for mid in movie_ids:
        try:
            rating = predict_base_pearson(uid, mid, rating_matrix, item_similarity)
        except Exception as e:
            print(e)
            break
        else:
            yield uid, mid, rating


def top_k_rs_mid(results, k):
    """按照预测的评分排序，取前k个预测结果的mid"""
    top_results = sorted(results, key=lambda x: x[2], reverse=True)[:k]
    return list(map(lambda x: x[1], top_results))


def item_based_CF(user_rating, uid, k):
    """
    基于物品的协同过滤推荐
    :param user_rating: 用户评分表
    :param uid: 当前用户ID
    :param k: 推荐的电影数量
    :return: k个电影id
    """
    rating_matrix = get_rating_matrix(user_rating)
    pearson_similarity = compute_pearson_similarity(rating_matrix)
    results = predict_all_base_pearson(uid, rating_matrix, pearson_similarity)
    mids = top_k_rs_mid(results, k)
    # 若皮尔逊相关系数没有相似用户(矩阵是稀疏的)，则使用余弦相似度来计算用户相似度
    # if not mids:
    #     print('余弦相似度:')
    #     mids = get_top_k_res(user_rating, uid, k)
    return mids


# ######################################


# def get_similar_matrix(favor_matrix, base='user'):
#     """基于用户或物品的相似度矩阵"""
#     if base == 'user':
#         user_similar = 1 - pairwise_distances(favor_matrix.values, metric='jaccard')
#         # print(user_similar)
#         similar_matrix = pd.DataFrame(user_similar, index=favor_matrix.index, columns=favor_matrix.index)
#         print(similar_matrix)
#     elif base == 'item':
#         item_similar = 1 - pairwise_distances(favor_matrix.values.T, metric='jaccard')
#         print(item_similar)
#         similar_matrix = pd.DataFrame(item_similar, index=favor_matrix.columns, columns=favor_matrix.columns)
#         print(similar_matrix)
#     else:
#         raise Exception("请输入正确的base, base=['user','item']")
#     return similar_matrix
#
#
# def find_N_similarity(similar_matrix, n=2):
#     """为每一个用户找到最相似的n个用户"""
#     topN_users = {}
#     for i in similar_matrix.index:
#         # 取出每一行数据，除去自己的一项，按照相似度排序
#         _df = similar_matrix.loc[i].drop([i])
#         _df_sorted = _df.sort_values(ascending=False)
#         topN = list(_df_sorted.index[:n])
#         topN_users[i] = topN
#     # print(topN_users)
#     return topN_users
#
#
# def recommend_result(topN_users):
#     """根据相似用户推荐给其他用户"""
#     rec_results = {}
#     for user, similar_users in topN_users.items():
#         result = set()
#         for similar_user in similar_users:
#             # print(df[df['user_id'] == similar_user]['favor_id'].values)
#             result = result.union(set(user_favor[user_favor['user_id'] == similar_user]['favor_id'].values))
#         # 过滤掉已经收藏过的电影
#         result -= set(user_favor[user_favor['user_id'] == user]['favor_id'].values)
#         rec_results[user] = list(result)[:5]
#     return rec_results


# #################################################################


def ItemSimilarity(train):
    # 物品-物品的共同矩阵
    C = dict()
    # 物品被多少个不同用户购买
    N = dict()
    for u, items in train.items():
        for i in items.keys():
            N.setdefault(i, 0)
            N[i] += 1
            C.setdefault(i, {})
            for j in items.keys():
                if i == j:
                    continue
                C[i].setdefault(j, 0)
                C[i][j] += 1
    # 计算相似度矩阵
    W = dict()
    for i, related_items in C.items():
        W.setdefault(i, {})
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    # print('相似度矩阵:',W)
    return W


# 推荐前K个电影
def Recommend(train, user_id, W, K):
    rank = dict()
    action_item = train[user_id]
    for item, score in action_item.items():
        for j, wj in sorted(W[item].items(), key=lambda x: x[1], reverse=True)[0:K]:
            if j in action_item.keys():
                continue
            rank.setdefault(j, 0)
            rank[j] += score * wj
    return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:K]


def get_top_k_res(user_rating, user_id, k):
    data = user_rating.drop(columns=['id', 'create_time'])
    data = data.loc[:, ['user_id', 'movie_id', 'star_rating']]
    train = dict()
    for user, item, score in data.itertuples(index=False):
        train.setdefault(user, {})
        train[user][item] = float(score)
    W = ItemSimilarity(train)
    result = Recommend(train, user_id, W, k)
    mids = list(map(lambda x:x[0], result))
    return mids


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
    sql = 'select * from user_favorites;'
    user_favor = pd.read_sql(sql, engine)

    sql = 'select * from user_rating;'
    user_rating = pd.read_sql(sql, engine)

    # 基于item-CF推荐电影
    # favor_matrix = load_data(data_path)
    # similarity = get_similar_matrix(favor_matrix)
    # topN_users = find_N_similarity(similarity)
    # rec_results = recommend_result(topN_users)
    # print(rec_results)

    # 基于item-CF推荐电影
    # data = pd.read_sql(sql, engine)
    # data.drop(columns=['id', 'create_time'], inplace=True)
    # data = data.loc[:, ['user_id', 'movie_id', 'star_rating']]
    # result = get_top_k_res(user_rating, 5, 10)
    # print(result)

    print(item_based_CF(user_rating, 2, 12))
