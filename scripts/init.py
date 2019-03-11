#!/usr/bin/env python

import os
import sys
import random

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")

django.setup()

from user.models import User
#from vip.models import Vip,Permission,VipPermRelation

last_names=(

        '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨',
        '朱秦尤许何吕施张孔曹严华金魏陶姜',
        '戚谢邹喻柏水窦章云苏潘葛奚范彭郎',
        '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐',
        '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常',
        '乐于时傅皮卞齐康伍余元卜顾孟平黄',
        '和穆萧尹姚邵湛汪祁毛禹狄米贝明臧',
        '计伏成戴谈宋茅庞熊纪舒屈项祝董梁',
        '杜阮蓝闵席季麻强贾路娄危江童颜郭',
        '梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍',
        '虞万支柯昝管卢莫经房裘缪干解应宗',
        '丁宣贲邓郁单杭洪包诸左石崔吉钮龚',
)

first_names={
    'male':[
        '梦文','幼芙','晓云','雨旋','秋安','雁风','碧槐','从海','语雪',
        '幼凡','秋卉','曼蕾','问蕾','访兰','寄莲','紫绿','新雁','恨容',
        '水柳','南云','曼阳','幼蓝','忆巧','灵荷','怜兰','听曼','碧双',
        '忆雁','夜松','映莲','听曼','秋易','绿莲','宛秋','雁安','问旋',
        '以蓝','若亦','幻丝','山凡','南云','寄蕊','绿春','思海','寄天',
        '友秋','紫玉','从筠','雪海','白筠','灵芙','安莲','惜梅','雪蕾',
    ],

    'female':[

        '秋枫','傲丝','春柔','冰岚','雅翠','易白','夜灵','静柔','醉绿',
        '乐蕊','寄蓝','乐彤','迎琴','之亦','雨寒','谷山','凝安','曼萍',
        '碧露','书南','山薇','念珊','芷雁','尔蕾','绮雪','傲萱','新琴',
        '绿蝶','慕旋','怀易','傲云','晓梅','诗菱','灵珊','幻香','若云',
        '如霜','晓晴','灵山','恨桃','梦凝','幻彤','觅波','慕玉','念山',
        '乐桃','语寒','怀海','孤蝶','灵凝','慕蓝','紫青','千兰','孤柔',
        '语曼','问海','寄筠','安露','听晴','冷寒','之翠','碧灵','凡丝',
    ]
}

def random_name():
    last_name=random.choice(random.choice(last_names))
    print(last_name)
    sex=random.choice(list(first_names.keys()))
    first_name=random.choice(first_names[sex])
    return ''.join([last_name,first_name]),sex

def create_robots(n):
    #创建初始用户
    for i in range(n):
        name,sex=random_name()

        try:
            User.objects.create(

                phonenum='%s'%random.randrange(21000000000,21900000000),
                nickname=name,
                sex=sex,
                birth_year=random.randint(1980,2000),
                birth_month=random.randint(1,12),
                birth_day=random.randint(1,28),
                location=random.choice(['bj','sh','gz','sz','cd','xa','wh',]),

            )
            print('created:%s %s'%(name,sex))
        except django.db.utils.IntegrityError:
            pass










if __name__=='__main__':
    create_robots(500)



















