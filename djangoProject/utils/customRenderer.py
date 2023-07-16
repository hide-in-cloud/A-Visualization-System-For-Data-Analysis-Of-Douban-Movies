"""
自定义返回处理结果
"""

from rest_framework.renderers import JSONRenderer


class MyJSONRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            # 判断实例的类型，返回的数据可能是列表也可能是字典
            if isinstance(data, dict):
                # 如果是字典的话应该是返回的数据，会包含msg,code,status等字段必须抽离出来
                msg = data.pop('message', 'success')
                # code: 200
                code = data.pop('code', renderer_context['response'].status_code)
                # 重新构建返回的JSON字典
            # data不是字典类型
            else:
                msg = 'success'
                code = renderer_context['response'].status_code
            # 自定义返回数据格式
            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)