import json
from django.http import HttpResponse
from django.conf import settings

def render_json(data=None,code=0):

    result={
        'data':data,
        'code':code,
    }

    if settings.DEBUG:
        json_str = json.dumps(result, ensure_ascii=False,indent=4,sort_keys=True) #缩进 格式化显示 按字母排序
    else:
        json_str=json.dumps(result,separators=(',',':')) # 修改分隔符
    return HttpResponse(json_str)
























