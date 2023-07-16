import os
import uuid

from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from user.models import UserInfo, UserToken, UserFavorites, UserRating
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework import serializers, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from utils.auth import LoginAuth
from utils.permission import MyPermission


class UserInfoSerializer(serializers.ModelSerializer):
    # allow_blank=False表示不能为空
    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[
                                         UniqueValidator(queryset=UserInfo.objects.all(), message="用户名已存在")])

    class Meta:
        model = UserInfo
        fields = '__all__'

    # TODO:密码加密


class UserInfoView(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    # 127.0.0.1:8000/api/user/usernameCount ---->get请求
    @action(methods=['GET'], detail=False)
    def usernameCount(self, request):
        """检查用户名是否重复"""
        username = request.GET.get('username')
        count = UserInfo.objects.filter(username=username).count()
        if count == 0:
            return Response(data={'msg': '用户名可用', 'res_code': 1, 'count': count})
        else:
            return Response(data={'msg': '用户名已存在', 'res_code': 0, 'count': count})

    # 127.0.0.1:8000/api/user/login ---->post请求
    @action(methods=['POST'], detail=False)
    def login(self, request):
        # post请求提交的数据都在request.data中
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')
        user = UserInfo.objects.all().filter(username=username, password=password, role=role).first()
        if user:
            # 登录成功，返回数据格式为 {code:100,msg:登录成功，token:'asdfasdf'}
            token = str(uuid.uuid4())
            # user=user，通过这个去查，如果能查到，使用defaults更新，如果查不到，使用所有新增
            UserToken.objects.update_or_create(defaults={'token': token}, user_id=user.id)
            return Response(data={'msg': '登录成功', 'res_code': 1, 'token': token})
        else:
            return Response(data={'msg': '用户名或密码错误', 'res_code': 0, 'token': ''})

    # 127.0.0.1:8000/api/user/info/?token=xxx ---->get请求
    @action(methods=['GET'], detail=False)
    def info(self, request):
        """ 根据token获取用户信息 """
        token = request.GET.get('token')
        if not token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})
        user_obj = UserToken.objects.filter(token=token).first().user
        if user_obj:
            # 序列化：将查询出来的obj转成json字典          manny=False -> 一个obj
            serializer = self.serializer_class(user_obj, many=False)
            return Response({'msg': 'OK', 'res_code': 1, 'data': serializer.data})
        else:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})

    # 127.0.0.1:8000/api/user/logout/ ----> post请求
    @action(methods=['POST'], detail=False)
    def logout(self, request):
        """ 用户退出登录 """
        token = request.data.get('token')
        UserToken.objects.filter(token=token).delete()
        return Response({'msg': '当前用户已注销', 'res_code': 1})

    # 127.0.0.1:8000/api/user/getSearchUsername/ ----> GET请求
    @action(methods=['GET'], detail=False)
    def getSearchUsername(self, request):
        """根据输入的关键词搜索相关用户名"""
        keyword = request.GET.get('keyword')
        if not keyword:
            return Response({'msg': '请输入关键字', 'res_code': 0, 'titles': []})
        user_qs = UserInfo.objects.filter(username__contains=keyword).all()
        data = []
        if user_qs:
            for user in user_qs:
                data.append(user.username)
        return Response({'msg': 'OK', 'res_code': 1, 'data': data})

    # 127.0.0.1:8000/api/user/favorIDList/?token=xxx ---->get请求
    @action(methods=['GET'], detail=False)
    def favorIDList(self, request):
        """ 根据token获取用户收藏夹的电影ID """
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})
        user_id = user_token.user.id
        favor_qs = UserFavorites.objects.filter(user_id=user_id).all()
        favor_list = []
        for obj in favor_qs:
            favor_list.append(obj.favor.id)
        return Response({'msg': 'OK', 'res_code': 1, 'data': favor_list})

    # 127.0.0.1:8000/api/user/favor/ ---->POST请求
    @action(methods=['POST'], detail=False)
    def favor(self, request):
        """ 根据用户点击收藏执行相应操作 """
        movie_id = request.GET.get('movie_id')
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if user_token:
            user_id = user_token.user.id  # 获取用户id
            # 如果收藏表中已收藏，则删除
            if UserFavorites.objects.filter(user_id=user_id, favor_id=movie_id).first():
                UserFavorites.objects.filter(user_id=user_id, favor_id=movie_id).delete()
                is_favor = False
            # 没有则创建一条收藏
            else:
                UserFavorites.objects.create(user_id=user_id, favor_id=movie_id)
                is_favor = True
            return Response({'msg': 'OK', 'res_code': 1, 'isFavor': is_favor})
        else:
            return Response({'msg': '您没有登录', 'res_code': 0, 'isFavor': None})

    # 127.0.0.1:8000/api/user/getUserFavor/?token=xxx ---->get请求
    @action(methods=['GET'], detail=False)
    def getUserFavor(self, request):
        """ 根据用户id和电影id获取用户评分信息 """
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})
        user_id = user_token.user.id
        movie_id = request.GET.get('movie_id')
        if UserFavorites.objects.filter(user_id=user_id, favor_id=movie_id).first():
            is_favor = True
        else:
            is_favor = False
        return Response({'msg': 'OK', 'res_code': 1, 'isFavor': is_favor})

    # 127.0.0.1:8000/api/user/getRatingIDList/?token=xxx ---->get请求
    @action(methods=['GET'], detail=False)
    def getRatingIDList(self, request):
        """ 根据token获取用户个人评分的电影ID """
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})
        user_id = user_token.user.id
        rating_qs = UserRating.objects.filter(user_id=user_id).all()
        rating_list = []
        for obj in rating_qs:
            rating_list.append(obj.movie.id)
        return Response({'msg': 'OK', 'res_code': 1, 'data': rating_list})

    # # 127.0.0.1:8000/api/user/userRating/ ---->POST请求
    @action(methods=['POST'], detail=False)
    def userRating(self, request):
        """ 根据用户评分执行相应操作 """
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})
        user_id = user_token.user.id  # 获取用户id

        movie_id = request.GET.get('movie_id')
        rating = request.GET.get('rating')
        # 如果评分表中已存在，则修改评分
        if UserRating.objects.filter(user_id=user_id, movie_id=movie_id).first():
            UserRating.objects.filter(user_id=user_id, movie_id=movie_id).update(star_rating=rating)
        # 没有则创建一条用户评分
        else:
            UserRating.objects.create(user_id=user_id, movie_id=movie_id, star_rating=rating)
        return Response({'msg': 'OK', 'res_code': 1, 'data': rating})

    # 127.0.0.1:8000/api/user/getUserRate/?token=xxx ---->get请求
    @action(methods=['GET'], detail=False)
    def getUserRate(self, request):
        """ 根据用户id和电影id获取用户评分信息 """
        token = request.GET.get('token')
        movie_id = request.GET.get('movie_id')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})
        user_id = user_token.user.id
        user_rating_qs = UserRating.objects.filter(user_id=user_id, movie_id=movie_id).first()
        if user_rating_qs is not None:
            rate = user_rating_qs.star_rating
            return Response({'msg': 'OK', 'res_code': 1, 'data': rate})
        else:
            return Response({'msg': 'OK', 'res_code': 1, 'data': None})

    # 127.0.0.1:8000/api/user/deleteUserRate/?token=xxx ---->post请求
    @action(methods=['POST'], detail=False)
    def deleteUserRate(self, request):
        """ 根据用户id和电影id删除对应的用户评分信息 """
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            return Response({'msg': '您没有登录', 'res_code': 0, 'data': {}})
        user_id = user_token.user.id
        movie_id = request.GET.get('movie_id')
        deleted, _ = UserRating.objects.filter(user_id=user_id, movie_id=movie_id).delete()
        print(deleted)
        if deleted:
            return Response({'msg': 'OK', 'res_code': 1})
        else:
            return Response({'msg': '删除失败', 'res_code': 0})


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'avatar']


class UserUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserUpdateSerializer
    authentication_classes = [LoginAuth]  # 登录认证

    # 127.0.0.1:8000/api/user_update/ ----> patch请求
    def patch(self, request, *args, **kwargs):
        """单个用户局部修改"""
        username = request.data.get('username')
        password = request.data.get('password')
        avatar = request.data.get('avatar')
        data = {}
        if username:
            data['username'] = username
        if password:
            data['password'] = password
        if avatar:
            data['avatar'] = avatar
        print(data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        # 如果有新头像，删除旧的头像
        if instance.avatar and avatar:
            os.remove(instance.avatar.path)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserPagination(PageNumberPagination):
    """ 自定义分页类 """
    page_size = 10
    page_query_param = 'page'  # url传过来的参数，表示第几页
    page_size_query_param = 'page_size'  # url传过来的参数，表示一页有多少数据
    max_page_size = 100


class UserInfoByPageView(ModelViewSet):
    """ 带 分页、模糊搜索 功能的movie """
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    authentication_classes = [LoginAuth]  # 登录认证
    permission_classes = [MyPermission]  # 权限
    pagination_class = UserPagination  # 配置自定义的分页器
    # 模糊搜索
    filter_backends = [SearchFilter]
    search_fields = ['username']  # 一个关键字同时对多个字段过滤


# class UserRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserRating
#         fields = '__all__'
#
#
# class UserRatingView(ModelViewSet):
#     queryset = UserRating.objects.all()
#     serializer_class = UserRatingSerializer
#     # authentication_classes = [LoginAuth]  # 登录认证
#     # permission_classes = [MyPermission]  # 权限
#
#     # 127.0.0.1:8000/api/user/rating/ ----> POST请求
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         return Response(serializer.data)
