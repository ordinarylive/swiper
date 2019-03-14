import  logging

from django.utils.deprecation import MiddlewareMixin

from common import errors

from libs.http import render_json
from user.models import User

err_log=logging.getLogger('err')


class AuthMiddleware(MiddlewareMixin):
    WHITE_LIST=[
        '/api/user/submit_phone',
        '/api/user/submit_vcode',
        '/api/vip/show_vip',
    ]
    def process_request(self,request):
        #当前url在白名单 最直接返回
        if  request.path in self.WHITE_LIST:
            return
        uid=request.session.get('uid')

        if  not  uid:
            #未登录 返回错误码
             return render_json(code=errors.LoginRequire.code)
        else:
            #已经登陆 取出user对象 并绑定到request对象
             request.user=User.get(id=uid)


class LogicErrorMiddleware(MiddlewareMixin):
    def process_exception(self,request,exception):
        if isinstance(exception,errors.LogicError):
            err_log.error(exception)

            return render_json(code=exception.code)
























