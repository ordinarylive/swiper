from django.shortcuts import render

# Create your views here.

## 接口规范

from django.http import JsonResponse
from django.core.cache import cache

from common import errors
from common import keys

from user.logics import send_vcode
from user.logics import is_phonenum
from libs.http import render_json

from user.models import User




def submit_phone(request):
    # 提交手机  发验证码
    phonenum = request.POST.get('phonenum')

    if is_phonenum(phonenum):
        # 生成验证码
        # 像短信平台发送验证码

        # 阿里云 https://www.aliyun.com/product/sms
        # 腾讯云 https://cloud.tencent.com/document/product/382
        # 网易云 https://netease.im/sms
        # 云之讯 https://www.ucpaas.com/
        # 互亿无线 http://www.ihuyi.com/

        if send_vcode(phonenum):
            return render_json()
        else:
            return render_json(code=errors.PLATFORM_ERR)
    else:
        return render_json(code=errors.PHONE_ERR)






def submit_vcode(request):
    #提交验证码 登录注册
    phone=request.POST.get('phonenum')
    vcode=request.POST.get('vcode')


    cached_vcode=cache.get(keys.VCODE%phone)
    if vcode == cached_vcode:
        user, _ = User.objects.get_or_create(phonenum=phone,
                                             nickname=phone)
        request.session['uid']=user.id
        return render_json(data=user.to_dict())

    else:
        return render_json(code=errors.VCODE_ERR)
















