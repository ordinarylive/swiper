from django.shortcuts import render
from libs.http import render_json
from vip.models import  Vip
from django.core.cache import cache
# Create your views here.

def show_vip(request):
    # 显示所有的vip的权限
    # 对于数据长期不变化的接口 适合添加长期缓存
    all_vip_info=cache.get('kkk')
    if  all_vip_info is None:

        all_vip_info=[]
        for vip in Vip.objects.all():
            vip_info=vip.to_dict()
            vip_info['perm']=[]
            for perm in  vip.perms():
                perm_info=perm.to_dict()
                vip_info['perm'].append(perm_info)

            all_vip_info.append(vip_info)

        cache.set('kkk',all_vip_info)


    return render_json(all_vip_info)































