import datetime
import time
from django.core.cache import cache

from common import keys
from swiper import config
from common import errors


from user.models import User
from social.models import Swiped, Friend


def  rcmd(user):
    #推荐算法

    today = datetime.date.today()
    max_year = today.year - user.profile.min_dating_age
    min_year = today.year - user.profile.max_dating_age

    #筛选出被用户滑过的sid列表
    user_swiped=Swiped.objects.filter(uid=user.id).only('sid')
    swiped_sid_list=[swiped.sid for swiped in user_swiped]

    # 取出满足条件用户
    users=User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__lte=max_year,
        birth_year__gte=min_year,
    ).exclude(id__in=swiped_sid_list)[:10]

    return users


def like_someone(user,sid):
    #添加滑动记录
    uid=user.id
    Swiped.swipe(uid=user.id,sid=sid,flag='like')
    # 检查对方是否喜欢本user#如果喜欢 建立好友关系
    if Swiped.is_liked(sid,uid):
        Friend.make_friends(uid,sid)
        #TODO：给对方 推送一条消息  通知新增了好友user  第三方平台 联系你喜欢的好友  进行提示
        return True
    return False


def superlike_someone(user,sid):
    # 添加滑动记录
    uid = user.id
    Swiped.swipe(uid=user.id, sid=sid, flag='superlike')
    # 检查对方是否喜欢本user#如果喜欢 建立好友关系
    if Swiped.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        # TODO：给对方 推送一条消息  通知新增了好友user  第三方平台 联系你喜欢的好友  进行提示
        return True
    return False

def rewind(user):
    #次数检查 一天只能3次反悔

    key=keys.REWIND_TIMES % user.id
    rewind_times = cache.get(key,0)
    if rewind_times >= config.REWIND_TIMES:
        raise errors.RewindLimit
    else:
        now = datetime.datetime.now()
        timeout = 86400-now.hour*3600-now.minute*60-now.second
        #通过时间戳计算剩余秒数
        #timeout=86400-(time.time()+3600*8)%86400
        cache.set(key,rewind_times + 1,timeout=timeout) #计数+1

    #取出上一次操作
    try:
        swiped=Swiped.objects.filter(uid=user.id).latest('time')
    except Swiped.DoesNotExist:
        return


    #检查上一次是否完成匹配
    if swiped.flag in ['like','superlike']:
        Friend.break_off(user.id,swiped.sid)

    swiped.delete()









































