from django.shortcuts import render

# Create your views here.
from libs.http import render_json

from social import logics
from social.models import Swiped
from user.models import User
from social.models import Friend
from vip.logics import need_perm



def rcmd_users(request):
    #获取推荐列表
    users=logics.rcmd(request.user)
    data=[user.to_dict() for user in users]
    return render_json(data)







@logics.add_swipe_score
def like(request):
    # 喜欢
    sid=int(request.POST.get('sid'))
    matched=logics.like_someone(request.user,sid)
    return render_json({'is_matched':matched})



@need_perm('superlike')
@logics.add_swipe_score
def superlike(request):
    sid=int(request.POST.get('sid'))
    matched = logics.superlike_someone(request.user, sid)

    return render_json({'is_matched': matched})







@logics.add_swipe_score
def dislike(request):
    sid=int(request.POST.get('sid'))
    Swiped.swipe(uid=request.user.id,sid=sid,flag='dislike')
    return render_json()





@need_perm('rewind')
def rewind(request):
    #返回接口   每天只允许反悔3次
    #返回操作 撤销上一次滑动操作
    #撤销上次操作
    logics.rewind(request.user)
    return render_json()


@need_perm('show_like_me')
def show_liked_me(request):
    uid_list = Swiped.who_liked_me(request.user.id)
    users=User.objects.filter(id__in=uid_list)
    user_info=[user.to_dict() for user in users]

    return render_json(user_info)



def friends(request):
    #查看好友列表  查看好友信息

    friend_id_list=Friend.friend_list(request.user.id)
    my_friends=User.objects.filter(id__in=friend_id_list)
    friend_info=[friend.to_dict() for friend in my_friends]

    return render_json(friend_info)


def friend_info(request):

    return render_json()


def top10(request):
    rank_data=logics.get_top_n(10)

    result = [[user.to_dict(),score] for user,score in rank_data]

    return render_json(result)


































