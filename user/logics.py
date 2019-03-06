
import re
from random import randint,randrange

import requests

from swiper import config


def is_phonenum(phonenum):
    pattern=r'(13\d|15[0123456789]|166|17[78]|18[0126789|199)\d{8}$'
    return True if re.match(pattern,phonenum) else False

def gen_random_code(length=4):
    code=randrange(10**length)
    template='%%0%dd'%length
    return template % code

# 调用云之讯接口
def send_vcode(phonenum):

    params=config.YZX_SMS_PARAMS.copy()
    params['param']=gen_random_code()
    params['mobile']=phonenum
    response = requests.post(config.YZX_SMS_API,json=params)

    if response.status_code==200:
        result=response.json()
        if result.get('msg')=='ok':
            return True
    return False







