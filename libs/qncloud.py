# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file
from swiper import config

def upload_qncloud(filename,filepath): #filename 上传后要保存的名字
    #上传文件到七牛云
    access_key = config.QN_ACCESS_KEY
    secret_key = config.QN_SECRET_KEY
    #构建鉴权对象
    qn_auth = Auth(access_key,secret_key)

    #生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(config.QN_BUCKET, filename, 3600)

    #执行上传过程
    ret, info = put_file(token, filename, filepath)
    return ret,info




















