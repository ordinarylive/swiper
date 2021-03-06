from django.shortcuts import render

# Create your views here.

## 接口规范

#django的cache只适用于本机的缓存  创建全局的缓存要用redis
from django.core.cache import cache
#常见的缓存系统
# 1.memcached  所有数据只保存在内存里  停机 进程关闭或者宕机 数据全部丢失  2.redis：性能高 支持数据持久化保存 程序启动 会将硬盘的数据全部加载到内存




import logging
from urllib.parse import urljoin
from common import errors
from common import keys
from libs.qncloud import upload_qncloud
from swiper import config

from user.logics import send_vcode, save_upload_file
from user.logics import is_phonenum
from user.logics import save_avatar
from libs.http import render_json




from user.models import User
from user.forms import ProfileForm

inf_log = logging.getLogger('inf')

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
            return render_json(code=errors.PlatformErr.code)
    else:
        return render_json(code=errors.PhoneErr.code)






def submit_vcode(request):
    #提交验证码 登录注册
    phone=request.POST.get('phonenum')
    vcode=request.POST.get('vcode')


    cached_vcode=cache.get(keys.VCODE%phone)
    if vcode == cached_vcode:
    # if  True:

        user, _ = User.get_or_create(phonenum=phone,
                                nickname=phone)

        inf_log.info(f'uid={user.id}')

        request.session['uid']=user.id
        return render_json(data=user.to_dict())

    else:
        return render_json(code=errors.VcodeErr.code)

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
    #定义key 从缓存获取
    key=keys.PROFILE%user.id

    profile_data = cache.get(key)

    print('get from cache:%s'%profile_data)


    #如果缓存没有  从数据库获取
    if profile_data is  None:
        profile_data=user.profile.to_dict('vibration','only_matche','auto_play')
        print(profile_data)
        print('get from DB:%s' % profile_data)
        cache.set(key,profile_data)
        #需要更新缓存
        print('set to cache')


    return render_json(profile_data)


#修改个人资料接口
def set_profile(request):
    form = ProfileForm(request.POST)
    if  form.is_valid():
        profile=form.save(commit=False) # 未添加到数据库  但得到profile模型对象
        profile.id=request.user.id
        profile.save()
        #数据发生变化后需要更新缓存

        key = keys.PROFILE % request.user.id
        profile_data = profile.to_dict('vibration', 'only_matche', 'auto_play')
        cache.set(key,profile_data)

        return render_json()
    else:
        return render_json(form.errors,code=errors.ProfileErr.code)





#上传个人头像接口
def upload_avatar(request):

    user=request.user
    avatar=request.FILES.get('avatar')
    #分块传入medias
    #定期清理medias中的文件

    #不用celery
    # filename='Avatar-%s'%user.id
    # filename,filepath=save_upload_file(filename,avatar)
    # upload_qncloud(filename,filepath)
    # user.avatar=urljoin(config.QN_HOST,filename)
    # user.save()

    #启用celery
    save_avatar.delay(user,avatar)
    return render_json()




