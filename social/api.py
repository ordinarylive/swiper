from django.shortcuts import render

# Create your views here.
from libs.http import render_json

from social import logics
from social.models import Swiped
from user.models import User


def rcmd_users(request):
    #获取推荐列表
    users=logics.rcmd(request.user)
    data=[user.to_dict() for user in users]
    return render_json(data)








def like(request):
    # 喜欢
    sid=int(request.POST.get('sid'))
    matched=logics.like_someone(request.user,sid)
    return render_json({'is_matched':matched})


def superlike(request):
    sid=int(request.POST.get('sid'))
    matched = logics.superlike_someone(request.user, sid)
    return render_json({'is_matched': matched})


def dislike(request):
    sid=int(request.POST.get('sid'))
    Swiped.swipe(uid=request.user.id,sid=sid,flag='dislike')
    return render_json()


def rewind(request):
    #返回接口   每天只允许反悔3次
    #返回操作 撤销上一次滑动操作
    #撤销上次操作
    logics.rewind(request.user)
    return render_json()



def show_liked_me(request):
    uid_list = Swiped.who_liked_me(request.user.id)
    users=User.objects.filter(id__in=uid_list)
    user_info=[user.to_dict() for user in users]

    return render_json(user_info)



def friends(request):
    return render_json()









































