import json
from django.http import HttpResponse


def render_json(data,code=0):

    result={
        'data':data,
        'code':code,
    }
    json_str=json.dumps(result,separators=(',',':')) # 修改分隔符
    return HttpResponse(json_str)
























