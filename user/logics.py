
import re
from random import randint,randrange

import requests
from django.core.cache import cache


from swiper import config
from common import keys

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







