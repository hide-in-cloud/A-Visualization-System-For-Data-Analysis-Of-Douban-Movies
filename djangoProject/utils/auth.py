from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import UserToken


class LoginAuth(BaseAuthentication):
    """ 认证类,校验用户是否登陆 """
    def authenticate(self, request):
        # token = request.query_params.get('token')  # 从get请求的地址中取
        # request.META   http请求头中的一些数据，HTTP_大写   HTTP_X_TOKEN
        token = request.META.get('HTTP_X_TOKEN')
        user_token = UserToken.objects.filter(token=token).first()
        # 有user_token说明用户已登录，放行
        if user_token:
            # 返回该token的用户和该token
            return user_token.user, token
            # 可通过 request.user, request.auth 获取到
        else:
            raise AuthenticationFailed('您没有登录')
