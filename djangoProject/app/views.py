# coding=UTF-8

import json
import os.path
from django.conf import settings
import jieba
from jieba.analyse import tfidf
from rest_framework.generics import GenericAPIView
from wordcloud import WordCloud
import pandas as pd
from sqlalchemy import create_engine
from app.models import MovieDetail, MovieComment
from user.models import UserToken, UserFavorites, UserRating
from utils.auth import LoginAuth
from utils.permission import MyPermission
from rest_framework import serializers, mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view  # 路由
from rest_framework.response import Response  # Json返回
from rest_framework.pagination import PageNumberPagination  # 分页
from rest_framework.filters import SearchFilter  # 模糊搜索(过滤)
from django_pandas.io import read_frame  # pandas.DataFrame
from app.recommend_base_content import RecommendBaseContent


# mysql驱动引擎
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
sql1 = 'select * from user_favorites;'
user_favor = pd.read_sql(sql1, engine)

sql2 = 'select * from user_rating;'
user_rating = pd.read_sql(sql2, engine)


def getMovieTypeDict(df):
    """统计每种类型的电影个数"""
    typeList = []  # 存放电影种类的列表
    for types in df['types'].values.tolist():
        typeList += types.split(',')
    # 统计每一类电影的个数
    type_dict = dict()
    for type in typeList:
        if type in type_dict:
            type_dict[type] += 1
        else:
            type_dict[type] = 1
    return type_dict


def getMovieCountryDict(df):
    """统计每个制片国家的电影个数"""
    countryList = []  # 存放电影种类的列表
    for countries in df['countries'].values.tolist():
        countryList += countries.split(',')
    # 统计每一类电影的个数
    country_dict = dict()
    for country in countryList:
        if country in country_dict:
            country_dict[country] += 1
        else:
            country_dict[country] = 1
    return country_dict


def getMovieLangDict(df):
    """统计每种语言的电影个数"""
    langList = []  # 存放电影种类的列表
    for lang in df['lang'].values.tolist():
        langList += lang.split(',')
    # 统计每一类电影的个数
    lang_dict = dict()
    for lang in langList:
        if lang in lang_dict:
            lang_dict[lang] += 1
        else:
            lang_dict[lang] = 1
    return lang_dict


class MovieInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = '__all__'


class MovieInfoView(ModelViewSet):
    """ movie信息 """
    queryset = MovieDetail.objects.all()
    serializer_class = MovieInfoSerializer
    authentication_classes = [LoginAuth]  # 登录认证
    # permission_classes = [MyPermission]  # 权限
    pagination_class = None  # 配置自定义的分页器
    filter_backends = [SearchFilter]
    search_fields = ['title']

    # coerce_float=True: 尝试将值转换为非字符串，将非数字对象（如decimal.Decimal）转化为浮点类型
    df = read_frame(qs=queryset, coerce_float=True)
    df['release_date'] = pd.to_datetime(df['release_date'])
    type_dict = getMovieTypeDict(df)
    country_dict = getMovieCountryDict(df)
    lang_dict = getMovieLangDict(df)
    # 推荐类
    recommendContent = RecommendBaseContent(df.copy(), user_favor, user_rating)

    # 127.0.0.1:8000/api/movie/info/homeInfo/ ---->get请求
    @action(methods=['GET'], detail=False)
    def homeInfo(self, request):
        columns = ['id', 'title', 'rate', 'release_date', 'comment_len', 'cover']
        df = self.df.copy()[columns]
        # 《天空之城》
        home_movie = df.loc[df['title'] == '天空之城']
        home_cover = home_movie['cover']

        # 评分最高电影
        # 查找rate最高的那一行数据
        highest_movie = df.loc[df['rate'].idxmax()]
        highest_movie = highest_movie.to_dict()

        # 最新电影
        # 查找上映日期最新的那一行数据
        latest_movie = df.loc[df['release_date'].idxmax()]
        latest_movie = latest_movie.to_dict()

        # 近期热门电影
        new_date = df['release_date'].max()  # 最新电影上映日期
        old_date = new_date - pd.Timedelta(60, unit='d')  # 最新日期往前60天
        recent_df = df[df['release_date'].between(old_date, new_date)]  # 取这区间的电影
        hot_movie = recent_df.loc[recent_df['comment_len'].idxmax()]  # 用评论数来定义热门电影
        hot_movie = hot_movie.to_dict()

        return Response(
            {'msg': 'OK', 'home_cover': home_cover, 'highest': highest_movie, 'latest': latest_movie, 'hot': hot_movie})

    # 127.0.0.1:8000/api/movie/info/getSearchTitles/ ---->get请求
    @action(methods=['GET'], detail=False)
    def getSearchTitles(self, request):
        """根据输入的关键词搜索相关电影名称"""
        keyword = request.GET.get('keyword')
        if not keyword:
            return Response({'msg': '请输入关键字', 'res_code': 0, 'titles': []})
        titles = self.df[self.df['title'].str.contains(keyword)]['title']
        if titles.empty:
            return Response({'msg': '没有相关电影', 'res_code': 0, 'titles': []})
        titles = titles.values.tolist()
        return Response({'msg': 'OK', 'res_code': 1, 'titles': titles})

    # 127.0.0.1:8000/api/movie/info/allMovieTypes/ ---->get请求
    @action(methods=['GET'], detail=False)
    def allMovieTypes(self, request):
        # 按每种类型的个数从多到少排序
        type_dict = sorted(self.type_dict.items(), key=lambda x: x[1], reverse=True)
        # 取出全部类型名称
        types = map(lambda x: x[0], type_dict)
        if types:
            return Response({'msg': 'OK', 'res_code': 1, 'types': types})
        else:
            return Response({'msg': 'Fail', 'res_code': 0, 'types': []})

    # 127.0.0.1:8000/api/movie/info/allMovieYears/ ---->get请求
    @action(methods=['GET'], detail=False)
    def allMovieYears(self, request):
        years = self.df['year'].unique().tolist()
        years = sorted(years, reverse=True)
        if years:
            return Response({'msg': 'OK', 'res_code': 1, 'years': years})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'years': []})

    # 127.0.0.1:8000/api/movie/info/allMovieCountries/ ---->get请求
    @action(methods=['GET'], detail=False)
    def allMovieCountries(self, request):
        """获取全部制片国家"""
        # 按每种制片国家的个数从多到少排序
        country_dict = sorted(self.country_dict.items(), key=lambda x: x[1], reverse=True)
        # 取出全部制片国家名称
        movie_countries = map(lambda x: x[0], country_dict)
        if movie_countries:
            return Response({'msg': 'OK', 'res_code': 1, 'countries': movie_countries})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'countries': []})

    # 127.0.0.1:8000/api/movie/info/allMovieLang/ ---->get请求
    @action(methods=['GET'], detail=False)
    def allMovieLang(self, request):
        """获取全部语言种类"""
        # 按每种语言的个数从多到少排序
        lang_dict = sorted(self.lang_dict.items(), key=lambda x: x[1], reverse=True)
        # 取出全部语言名称
        movie_langs = map(lambda x: x[0], lang_dict)
        if movie_langs:
            return Response({'msg': 'OK', 'res_code': 1, 'langs': movie_langs})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'langs': []})

    # 127.0.0.1:8000/api/movie/info/recommendBaseContent/ ---->GET请求
    @action(methods=['GET'], detail=False)
    def recommendBaseContent(self, request):
        """ 基于电影内容的推荐 """
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': []})
        user_id = user_token.user.id  # 获取用户id
        # 用户收藏的电影ID
        favor_qs = UserFavorites.objects.filter(user_id=user_id).all()
        favor_mid = set()
        for qs in favor_qs:
            favor_mid.add(qs.favor_id)
        # 用户评分过的电影ID
        rating_qs = UserRating.objects.filter(user_id=user_id).all()
        rating_mid = set()
        for qs in rating_qs:
            rating_mid.add(qs.movie_id)
        # 合并两个电影id集合
        mids = list(favor_mid.union(rating_mid))
        self.recommendContent.update_user_profile(user_id, mids)
        # print(self.recommendContent.user_profile[user_id])
        data = self.recommendContent.predict_user_movies(user_id, k=12)
        if data:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': []})

    # 127.0.0.1:8000/api/movie/info/recommendBaseUserCF/ ---->GET请求
    @action(methods=['GET'], detail=False)
    def recommendBaseUserCF(self, request):
        """ 基于 user-base CF 的推荐 """
        from .userCF import user_based_CF
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': []})
        user_id = user_token.user.id  # 获取用户id

        user_rating = pd.read_sql(sql2, engine)
        result = user_based_CF(user_rating, user_id, k=12)
        # print(result)
        if result:
            return Response({'msg': 'OK', 'res_code': 1, 'data': result})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': []})

    # 127.0.0.1:8000/api/movie/info/recommendBaseItemCF/ ---->GET请求
    @action(methods=['GET'], detail=False)
    def recommendBaseItemCF(self, request):
        """ 基于 item-base CF 的推荐 """
        from .itemCF import get_top_k_res, item_based_CF
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': []})
        user_id = user_token.user.id  # 获取用户id

        user_rating = pd.read_sql(sql2, engine)
        result = item_based_CF(user_rating, user_id, 12)
        if result:
            return Response({'msg': 'OK', 'res_code': 1, 'data': result})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': []})


# #####################  修改电影  ###########################

class MovieUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = ['title','types','year','directors','actors','summary','rate','detail_url',
                  'countries','lang','release_date','runtime']


class MovieUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = MovieDetail.objects.all()
    serializer_class = MovieUpdateSerializer
    authentication_classes = [LoginAuth]  # 登录认证

    #  ----> patch请求
    def patch(self, request, *args, **kwargs):
        """单个电影局部修改"""
        title = request.data.get('title')
        types = request.data.get('types')
        year = request.data.get('year')
        directors = request.data.get('directors')
        actors = request.data.get('actors')
        summary = request.data.get('summary')
        rate = request.data.get('rate')
        detail_url = request.data.get('detail_url')
        countries = request.data.get('countries')
        lang = request.data.get('lang')
        release_date = request.data.get('release_date')
        runtime = request.data.get('runtime')
        data = {}
        if title:
            data['title'] = title
        if types:
            data['types'] = types
        if year:
            data['year'] = year
        if directors:
            data['directors'] = directors
        if actors:
            data['actors'] = actors
        if summary:
            data['summary'] = summary
        if rate:
            data['rate'] = rate
        if detail_url:
            data['detail_url'] = detail_url
        if countries:
            data['countries'] = countries
        if lang:
            data['lang'] = lang
        if release_date:
            data['release_date'] = release_date
        if runtime:
            data['runtime'] = runtime
        print(data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# ######################### page #############################


class MoviePagination(PageNumberPagination):
    """ 自定义分页类 """
    page_size = 10              # 每页展示多少条数据
    page_query_param = 'page'   # url传过来的参数，表示第几页
    page_size_query_param = 'page_size'  # url传过来的参数，表示一页有多少数据
    max_page_size = 100


class MovieInfoByPageView(ModelViewSet):
    """ 带 分页、模糊搜索 功能的movie """
    queryset = MovieDetail.objects.all()
    serializer_class = MovieInfoSerializer
    authentication_classes = [LoginAuth]  # 登录认证
    permission_classes = [MyPermission]  # 权限
    pagination_class = MoviePagination  # 配置自定义的分页器
    # 模糊搜索
    filter_backends = [SearchFilter]
    search_fields = ['title']  # 一个关键字同时对多个字段过滤

    def get_queryset(self):
        """过滤字段"""
        types = self.request.query_params.get('types')
        year = self.request.query_params.get('year')
        country = self.request.query_params.get('country')

        queryset = MovieDetail.objects.all()
        if types is not None:
            queryset = queryset.filter(types__icontains=types)
        if year is not None:
            queryset = queryset.filter(year__icontains=year)
        if country is not None:
            queryset = queryset.filter(countries__icontains=country)
        return queryset


# ######################## chart ##############################


from pyecharts.charts import Pie, Bar
from pyecharts import options as opts
import numpy as np


def pie_base(title, data_pair) -> Pie:
    """ 为饼状图返回一个option """
    pie = (
        Pie()
        .add('', data_pair=data_pair)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="right", orient="vertical"),
        )
        .set_series_opts(tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"))
        .dump_options_with_quotes()
    )
    return pie


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = ['types', 'rate', 'runtime', 'year', 'actors']


class ChartView(ModelViewSet):
    """ movie图表 """
    queryset = MovieDetail.objects.all()
    serializer_class = ChartSerializer
    df = read_frame(qs=queryset, coerce_float=True)
    df['release_date'] = pd.to_datetime(df['release_date'])
    type_dict = getMovieTypeDict(df)

    # 127.0.0.1:8000/api/movie/chart/typesDistribution/ ---->get请求
    @action(methods=['GET'], detail=False)
    def typesDistribution(self, request):
        """ 获取电影各类型分布占比的数据 """
        data_pair = list(self.type_dict.items())  # [(k,v),(k,v),(k,v)]
        if data_pair:
            return Response({'msg': 'OK', 'res_code': 1, 'data': json.loads(pie_base('电影类型分布饼状图', data_pair))})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/movie/chart/rateDistribution/ ---->get请求
    # @action(methods=['GET'], detail=False)
    # def rateDistribution(self, request):
    #     """ 获取电影各评分分布直方图的数据 """
    #     df = read_frame(qs=self.queryset, index_col='id', fieldnames=['rate'], coerce_float=True)
    #     # rate_list = df['rate'].values.tolist()  # 存放各电影评分的列表
    #     max_rate = df['rate'].max()  # 最高评分
    #     min_rate = df['rate'].min()  # 最低评分
    #     # 右边界取最高评分的向上取整0.5
    #     if math.ceil(max_rate) - max_rate >= 0.5:
    #         right = int(max_rate) + 0.5
    #     else:
    #         right = math.ceil(max_rate)
    #     # 左边界取最低评分的向下取整0.5
    #     if min_rate - int(min_rate) >= 0.5:
    #         left = int(min_rate) + 0.5
    #     else:
    #         left = int(min_rate)
    #     bins = int((right - left) // 0.5)  # 计算划分成几个区间，每个区间长度为0.5
    #     rate_bins = [left+0.5*i for i in range(bins+1)]  # 自定义区间
    #     df['rate_range'] = pd.cut(df['rate'], rate_bins, right=False)  # 划分数据
    #     counts = df['rate_range'].value_counts(sort=False)
    #     x_data = counts.index.map(lambda x: str(x)).tolist()
    #     print(x_data)
    #     y_data = counts.values.tolist()  # 统计每个区间的数据个数
    #     data = {
    #         'x_data': x_data,
    #         'y_data': y_data
    #     }
    #     if y_data:
    #         return Response({'msg': 'OK', 'res_code': 1, 'data': data})
    #     else:
    #         return Response({'msg': '未查到数据', 'res_code': 0, 'data': data})

    # 127.0.0.1:8000/api/movie/chart/rateDistribution/ ---->get请求
    @action(methods=['GET'], detail=False)
    def rateDistribution(self, request):
        """ 获取电影各评分分布折线面积图的数据 """
        df = read_frame(qs=self.queryset, fieldnames=['rate'], coerce_float=True)
        rate_list = df['rate'].values.tolist()  # 存储每一个电影的评分
        rate_list.sort()  # 从低到高排序
        rate_dict = {}  # 统计每个评分的电影数目
        for rate in rate_list:
            if rate in rate_dict:
                rate_dict[rate] += 1
            else:
                rate_dict[rate] = 1
        data = {
            'x_data': list(rate_dict.keys()),
            'y_data': list(rate_dict.values())
        }
        if rate_dict:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': data})

    # 127.0.0.1:8000/api/movie/chart/runtimeDistribution/ ---->get请求
    @action(methods=['GET'], detail=False)
    def runtimeDistribution(self, request):
        """ 获取各电影时长分布占比的数据 """
        columns = ['runtime']
        df = self.df.copy()[columns]
        runtime_bins = [0, 60, 120, 180, np.inf]  # 自定义时长区间
        df['runtime_label'] = pd.cut(df['runtime'], runtime_bins, right=False, labels=["短(<60分钟)", "中(60-120分钟)", "长(120-180分钟)", '特长(>180分钟)'])
        runtime_dict = df['runtime_label'].value_counts(sort=False).to_dict()
        data_pair = list(runtime_dict.items())
        if data_pair:
            return Response({'msg': 'OK', 'res_code': 1, 'data': json.loads(pie_base('电影时长分布饼状图', data_pair))})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/movie/chart/timeLine/ ---->get请求
    @action(methods=['GET'], detail=False)
    def timeLine(self, request):
        """ 获取每一年的电影平均评分折线图的数据 """
        columns = ['rate', 'year', 'countries']
        df = self.df.copy()[columns]
        df = df[df['year'] >= str(1988)]
        # 获取全球每一年的电影平均评分
        mean_rate_world_dict = df.groupby('year')['rate'].mean().round(2).to_dict()
        # 获取中国每一年的电影平均评分
        df_china = df[df['countries'].str.contains('中国')]
        mean_rate_china_dict = df_china.groupby('year')['rate'].mean().round(2).to_dict()
        # 获取美国每一年的电影平均评分
        df_america = df[df['countries'].str.contains('美国')]
        mean_rate_america_dict = df_america.groupby('year')['rate'].mean().round(2).to_dict()
        # 填充某些年份的空值
        for k, v in mean_rate_world_dict.items():
            if k not in mean_rate_china_dict:
                mean_rate_china_dict[k] = "-"
            if k not in mean_rate_america_dict:
                mean_rate_america_dict[k] = "-"
        # 按年份排序
        mean_rate_china_dict = dict(sorted(mean_rate_china_dict.items(), key=lambda x: x[0]))
        mean_rate_america_dict = dict(sorted(mean_rate_america_dict.items(), key=lambda x: x[0]))
        data = {
            'world': {
                'x_data': list(mean_rate_world_dict.keys()),
                'y_data': list(mean_rate_world_dict.values())
            },
            'china': {
                'x_data': list(mean_rate_china_dict.keys()),
                'y_data': list(mean_rate_china_dict.values())
            },
            'america': {
                'x_data': list(mean_rate_america_dict.keys()),
                'y_data': list(mean_rate_america_dict.values())
            }
        }
        if mean_rate_world_dict:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/movie/chart/rateSort/?start_year ---->get请求
    @action(methods=['GET'], detail=False)
    def rateSort(self, request):
        """ 获取其中10年的TOP10电影的数据 """
        start_year = request.data.get('start_year', 2014)
        columns = ['title', 'rate', 'year', 'release_date']
        df = self.df.copy()[columns]
        data = []  # 存放十年的数据
        # 查询10年的TOP10电影
        for i in range(10):
            current_year = start_year + i
            # 按评分排序查找前10名
            df_sort_rate = df[df['year'] == str(current_year)].sort_values('rate', ascending=False)
            if df_sort_rate.shape[0] >= 10:
                top10 = df_sort_rate.iloc[:10]
            else:
                top10 = df_sort_rate.iloc[:df_sort_rate.shape[0]]
            x_data = top10['rate'].tolist()[::-1]  # TOP10电影评分，倒序排放
            y_data = top10['title'].tolist()[::-1]  # TOP10电影名称，倒序排放
            series_data = []
            # 组合成一个二维列表
            for j in range(len(y_data)):
                series_data.append([x_data[j], y_data[j]])
            data.append(series_data)
        # print(data)
        if data:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/movie/chart/badMovie/ ---->get请求
    @action(methods=['GET'], detail=False)
    def badMovie(self, request):
        """ 获取电影烂片数量及占比的年变化的数据 """
        columns = ['title', 'rate', 'year']
        df = self.df.copy()[columns]
        # 先筛选出烂片(评分低于6.0)，再按照年份分组
        bad_movie = df[df['rate'] < 6]
        bad_count_dict = bad_movie.groupby('year')['rate'].count().to_dict()

        proportion = []  # 烂片占比
        # 遍历字典中每一年，算出总数，再算出烂片占比
        for key, val in bad_count_dict.items():
            movie_sum = df[df['year'] == key]['rate'].count()  # 每年电影总数
            proportion.append((val / movie_sum).round(2))  # 烂片占比
        data = {
            'year': bad_count_dict.keys(),
            'count': bad_count_dict.values(),
            'proportion': proportion,
        }
        if data:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/movie/chart/countrySort ---->get请求
    @action(methods=['GET'], detail=False)
    def countrySort(self, request):
        """ 获取各个国家的总电影数 """
        columns = ['title', 'rate', 'year', 'countries']
        df = self.df.copy()[columns]
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')
        if start_year:
            df = df[df['year'] >= str(start_year)]
        if end_year:
            df = df[df['year'] <= str(end_year)]
        # 统计每一个国家的电影总数
        country_dict = getMovieCountryDict(df)
        # 按每个国家的电影数排序，取前15个国家
        country_dict = dict(sorted(country_dict.items(), key=lambda x: x[1], reverse=True)[:15])
        # 统计每一个国家的优秀电影总数(评分在7.5分以上)
        df = df[df['rate'] >= 7.5]
        good_count = []
        for country in country_dict.keys():
            good_count.append(df[df['countries'].str.contains(country)]['title'].count())
        data = {
            'countries': country_dict.keys(),
            'count': country_dict.values(),
            'good_count': good_count
        }
        if data:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/movie/chart/directorSort ---->get请求
    @action(methods=['GET'], detail=False)
    def directorSort(self, request):
        """ 获取优秀导演的平均评分及总电影数 """
        columns = ['title', 'rate', 'directors']
        df = self.df.copy()[columns]
        director_list = []  # 存放各导演的列表
        for directors in df['directors'].values.tolist():
            director_list += directors.split(',')
        # 统计每一个导演的电影数
        director_dict = dict()
        for director in director_list:
            if director in director_dict:
                director_dict[director] += 1
            else:
                director_dict[director] = 1
        # 筛选出电影数大于5的导演
        top_directors = dict(filter(lambda x: x[1] >= 5, director_dict.items()))
        # 每个导演的平均评分
        mean_rate_dict = {}
        for key in top_directors.keys():
            mean_rate_dict[key] = df[df['directors'].str.contains(key)]['rate'].mean().round(2)
        # 按平均评分排序
        mean_rate_dict = dict(sorted(mean_rate_dict.items(), key=lambda x: x[1], reverse=True))
        # 按评分排序获取对应电影数量
        movie_sum = []
        for key in mean_rate_dict.keys():
            movie_sum.append(top_directors[key])
        data = {
            'directors': mean_rate_dict.keys(),
            'movie_sum': movie_sum,
            'mean_rate': mean_rate_dict.values()
        }
        if data:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/movie/chart/actorSort ---->get请求
    @action(methods=['GET'], detail=False)
    def actorSort(self, request):
        """ 获取各演员出场次数排名 """
        columns = ['title', 'rate', 'actors']
        df = self.df.copy()[columns]
        # 将每一行演员转成列表
        df['actors'] = df['actors'].apply(lambda x: x.split(',') if x is not None else [])

        actor_list = []  # 存放各演员的列表
        for index,value in df['actors'].items():
            try:
                print(value)  # 不能注释，不能删！
                actor_list += value
            except Exception as e:
                print(index)
                continue

        # 统计每一个演员的出场数
        actor_dict = dict()
        for actor in actor_list:
            if actor in actor_dict:
                actor_dict[actor] += 1
            else:
                actor_dict[actor] = 1
        # 筛选出出场次数大于10的演员
        actor_dict = dict(filter(lambda x: x[1] >= 10, actor_dict.items()))
        # 按演员出场次数排序,取前25名演员
        k = 25
        data = list(sorted(actor_dict.items(), key=lambda x: x[1], reverse=True)[:k])
        if data:
            return Response({'msg': 'OK', 'res_code': 1, 'data': data})
        else:
            return Response({'msg': '未查到数据', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/movie/chart/getWordCloud ---->get请求
    @action(methods=['GET'], detail=False)
    def getWordCloud(self, request):
        """ 获取用户评论词云图 """
        title = request.GET.get('title')
        if title is not None:
            columns = ['id','title']
            df_movie = self.df.copy()[columns]
            movie_id = df_movie[df_movie['title'] == title]['id']
            if movie_id.empty:
                return Response({'msg': '请输入正确的完整的电影名称', 'res_code': 0, 'data': {}})
            movie_id = movie_id.values[0]
            # print(movie_id)

            # 查询该电影的评论
            # TODO:一对多表查询
            # comment_qs = MovieComment.objects.all()
            # df_comment = read_frame(qs=comment_qs, coerce_float=True)
            engine = create_engine('mysql+pymysql://root:123456@localhost:3306/douban_movie')
            sql = 'select * from movie_comment;'
            df_comment = pd.read_sql(sql, engine)
            comment_content = df_comment[df_comment['movie_id'] == movie_id]['comment_content']
            if comment_content.empty:
                return Response({'msg': '尚未有用户评论', 'res_code': 0, 'data': {}})
            # 用jieba分词库对评论内容进行分词
            comment = ''  # 合并用户评论内容
            for val in comment_content.values:
                try:
                    val = json.loads(val)
                    print(val)  # 不能注释，不能删！
                    comment += val
                except Exception as e:
                    pass
                    continue
            cut = jieba.cut(comment)  # 分词
            words = ' '.join(cut)
            words = tfidf(words)  # 词分析，过滤掉日常用语，筛选关键词
            text = ' '.join(words)
            # 生成词云图
            wc = WordCloud(
                background_color='white',
                font_path='msyh.ttc'
            )
            wc.generate_from_text(text)
            directory_path = f'./media/wordcloud_comment/{title}'  # 图片存放的文件夹
            if not os.path.exists(directory_path):  # 若路径不存在，则新建文件夹
                os.makedirs(directory_path)
            wc.to_file(os.path.join(directory_path, 'wc_img.png'))  # 保存图片文件
            # 返回给前端的路径
            img_path = os.path.join(settings.MEDIA_URL,'wordcloud_comment', title, 'wc_img.png')
            return Response({'msg': 'OK', 'res_code': 1, 'img': img_path})
        return Response({'msg': '请输入电影名称', 'res_code': 0, 'data': {}})
