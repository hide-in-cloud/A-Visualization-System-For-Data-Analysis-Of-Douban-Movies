from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(err, context: dict):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(err, context)

    if response is None:
        return Response({
            'message': f'服务器错误:{err}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        res = {'message': response.reason_phrase}
        res.update(response.data)
        return Response(res, status=response.status_code, exception=True)
