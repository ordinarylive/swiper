from django.shortcuts import render

# Create your views here.

## 接口规范

from django.http import JsonResponse

from common import errors
from user.logics import send_vcode
from user.logics import is_phonenum
from libs.http import render_json



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
            return render_json(None)
        else:
            return render_json(None,errors.PLATFORM_ERR)
    else:
        return render_json(None,errors.PHONE_ERR)






def submit_vcode(request):
    #phone
    #vcode

    return












