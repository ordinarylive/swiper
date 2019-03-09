from django.db import models

# Create your models here.

class Swiped(models.Model):
    # uid sid type time
    FLAG=(
        ('like','喜欢'),
        ('superlike','超级喜欢'),
        ('dislike','不喜欢'),
    )


    uid=models.IntegerField(verbose_name='滑动着的uid')
    sid=models.IntegerField(verbose_name='被滑动着的sid')
    flag=models.CharField(max_length=16,choices=FLAG,verbose_name='滑动类型')
    time=models.DateTimeField(auto_now_add=True,verbose_name='滑动的时间')














    