from django.shortcuts import render

# Create your views here.

## 接口规范


from django.core.cache import cache



from common import errors
from common import keys

from user.logics import send_vcode
from user.logics import is_phonenum
from user.logics import save_avatar
from libs.http import render_json




from user.models import User
from user.forms import ProfileForm



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

'''
http 过程
1.wsgi   web  serverce gateway interface 将请求报文封装成HttpRequest对象
---------------------》 process_request（切面）
2.URL   映射
——————————————》process_view（切面）
3.执行view函数
4.获取参数
5.执行逻辑处理 进行数据库 缓存等
——————————————————————》process_template（切面）
6.模板渲染
7.封装HttpResponse对象
——————————————————————————》process_response处理响应之前（切面）
8.将HttpResponse 对象转化为HTTP响应报文
9.将报文发送到浏览器


中间件 面向切面
process_request
process_view
process_template
process_exception 报错产生的切面
process_response



'''


#获取个人资料接口
def get_profile(request):
    user=request.user
    profile_data=user.profile.to_dict('vibration','only_matche','auto_play')
    return render_json(profile_data)


#修改个人资料接口
def set_profile(request):
    form = ProfileForm(request.POST)
    if  form.is_valid():
        profile=form.save(commit=False) # 未添加到数据库  但得到profile模型对象
        profile.id=request.user.id
        profile.save()
        return render_json()
    else:
        return render_json(form.errors,code=errors.PROFILE_ERR)





#上传个人头像接口
def upload_avatar(request):

    user=request.user
    avatar=request.FILES.get('avatar')
    #分块传入medias
    #定期清理medias中的文件

    save_avatar.delay(user,avatar)
    return render_json()




