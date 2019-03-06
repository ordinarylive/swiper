from django.db import models

# Create your models here.
class User(models.Model):
    SEX=(
        ('male','男性'),
        ('female','女性'),
    )

    LOCATION=(
        ('bj', '北京'),
        ('sh', '上海'),
        ('gz', '广州'),
        ('sz', '深圳'),
        ('cd', '成都'),
        ('xa', '西安'),
        ('wh', '武汉'),
    )


    phonenum=models.CharField(max_length=16,unique=True,verbose_name='手机号')
    nickname=models.Field(max_length=32,unique=True,verbose_name='昵称')
    sex=models.Field(max_length=8,choices=SEX,verbose_name='性别')
    birth_year=models.Field(default=2000,verbose_name='出生年')
    birth_month=models.Field(default=1,verbose_name='出生月')
    birth_day=models.Field(default=1,verbose_name='出生日')
    avatar=models.Field(max_length=256,verbose_name='个人头像')
    location=models.Field(max_length=16,choices=LOCATION,verbose_name='常居地')
































