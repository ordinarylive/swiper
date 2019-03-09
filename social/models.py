from django.db import models
from common import errors
# Create your models here.

class Swiped(models.Model):
    # uid sid type time
    FLAGS=(
        ('like','喜欢'),
        ('superlike','超级喜欢'),
        ('dislike','不喜欢'),
    )


    uid=models.IntegerField(verbose_name='滑动着的uid')
    sid=models.IntegerField(verbose_name='被滑动着的sid')
    flag=models.CharField(max_length=16,choices=FLAGS,verbose_name='滑动类型')
    time=models.DateTimeField(auto_now_add=True,verbose_name='滑动的时间')


    @classmethod
    def swipe(cls,uid,sid,flag):
        # 记录滑动操作 不允许重复滑动某一个人
        flags=[_flag for _flag, _ in cls.FLAGS]
        if flag not in flags:
            raise  errors.FlagErr()
        cls.objects.update_or_create(uid=uid,sid=sid,defaults={'flag':flag})


    @classmethod
    def is_liked(cls,uid,sid):
        return cls.objects.filter(uid=uid,sid=sid,flag__in=['like','superlike']).exists()








class Friend(models.Model):
    '好友关系表'
    uid1=models.IntegerField()

    uid2=models.IntegerField()


    @classmethod
    def make_friends(cls,uid1,uid2):
        # 建立好友关系
        uid1,uid2 =  (uid2,uid1)   if uid1 >uid2 else (uid1,uid2)
        cls.objects.get_or_create(uid1=uid1,uid2=uid2)






































