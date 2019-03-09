
import re
import os
from random import randint,randrange
from urllib.parse import urljoin


import requests
from django.core.cache import cache
from django.conf import settings

from swiper import config
from common import keys
from libs.qncloud import  upload_qncloud
from worker import celery_app


def is_phonenum(phonenum):
    print(phonenum,type(phonenum))
    pattern=r'^1([38]\d|5[0-35-9]|7[3678])\d{8}$'
    return True if re.match(pattern,phonenum) else False

def gen_random_code(length=4):
    code=randrange(10**length)
    template='%%0%dd'%length
    return template % code

# 调用云之讯接口
def send_vcode(phonenum):

    vcode=gen_random_code()
    cache.set(keys.VCODE % phonenum,vcode,180)


    params=config.YZX_SMS_PARAMS.copy()
    params['param']=vcode
    params['mobile']=phonenum
    response = requests.post(config.YZX_SMS_API,json=params)

    if response.status_code==200:
        result=response.json()
        print(result)
        if result.get('msg')=='OK':
            return True
    return False



def save_upload_file(filename,upload_file):
    #保存上传的文件到本地
    filepath =os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,filename)
    with  open(filepath,'wb') as newfile:
        for  chunk in upload_file.chunks():
            newfile.write(chunk)
    return filename,filepath


@celery_app.task
def  save_avatar(user,avatar):
    #保存用户形象
    filename = 'Avatar-%s' % user.id
    filename, filepath = save_upload_file(filename, avatar)

    # 上传到七牛云
    upload_qncloud(filename, filepath)

    # 记录头像URL地址
    user.avatar = urljoin(config.QN_HOST, filename)
    user.save()



