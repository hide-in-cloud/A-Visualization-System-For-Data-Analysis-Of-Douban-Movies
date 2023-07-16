from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    """ 权限校验 """
    def has_permission(self, request, view):
        from django.conf import settings

        # 1.获取当前用户所有权限
        # print(request.user.role)  # 获取用户角色
        permission_dict = settings.PERMISSION[request.user.role]

        # 2.当前用户正在访问的url和方式
        url_name, method = request.resolver_match.url_name, request.method

        # 3.权限判断
        method_list = permission_dict.get(url_name)
        if not method_list:
            return False
        if method in method_list:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # 视图中 self.get_object()
        return True
