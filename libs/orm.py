

#以中间件的方式 将数据以字典输出
# class ModelMixin:
#     def to_dict(self,*exclude):
#         #将model对象转换为属性字典  exclude 需要排除的字段
#         attr_dict={}
#         for field in  self._meta.fields:
#             field_name=field.attname
#             if field_name not in exclude:
#                 attr_dict[field_name]=getattr(self,field_name)
#         return attr_dict




from django.db import models
from django.core.cache import cache
from common import keys

#修改models底层 对输出数据 dict化
def to_dict(self,*exclude):
    #将model对象转换为属性字典  exclude 需要排除的字段
    attr_dict={}
    for field in  self._meta.fields:
        field_name=field.attname
        print(field_name)
        if field_name not in exclude:
            attr_dict[field_name]=getattr(self,field_name)
            print(attr_dict)

    return attr_dict


#对models模型添加新的方法 将create get save的返回数据存到 全局redis缓存中 以便 直接从缓存中拿去数据 从而减少对数据库的IO操作
#类方法
def get(cls,*args,**kwargs):
    '''先缓存中获取数据 如果缓存中没有 则从数据库获取'''
    pk=kwargs.get('id') or kwargs.get('pk') #获取主键
    if pk is not None:
        key = keys.MODEL % (cls.__name__, pk)  # 定义缓存key
        #从缓存中获取数据
        model_obj=cache.get(key)
        if isinstance(model_obj,cls): #判断是否属于该类
            return model_obj

    #缓存里没有 从数据库获取
    model_obj=cls.objects.get(*args,**kwargs)
    #将取出的数据写入缓存
    key=keys.MODEL%(cls.__name__,model_obj.pk)
    cache.set(key,model_obj)
    return model_obj




def get_or_create(cls,defaults=None,**kwargs):
    '''为objects.get_or_create 添加缓存的处理'''

    pk = kwargs.get('id') or kwargs.get('pk')  # 获取主键
    if pk is not None:
        key = keys.MODEL % (cls.__name__, pk)  # 定义缓存key
        # 从缓存中获取数据
        model_obj = cache.get(key)
        if isinstance(model_obj, cls):  # 判断是否属于该类
            return model_obj,False

    # 缓存里没有 从数据库获取
    model_obj,created = cls.objects.get_or_create(defaults,**kwargs)
    # 将取出的数据写入缓存
    key = keys.MODEL % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj)
    return model_obj,created


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    #添加了缓存处理的save方法
    #先将数据 通过原save方法保存到数据库
    self._save(force_insert, force_update, using,
         update_fields)

    #将model对象写入缓存
    key=keys.MODEL%(self.__class__.__name__,self.pk)
    cache.set(key,self)




#对model做补丁    动态对model方法做补丁 此方法为MonkeyPatch方法  动态补丁方法
def patch_model():
    #为model对象打补丁
    # 动态Model 增加新类方法
    models.Model.to_dict=to_dict
    models.Model.get=classmethod(get) #转为类方法
    models.Model.get_or_create=classmethod(get_or_create)

    # 修改原save方法
    models.Model._save =models.Model.save  #将原save方法做备份
    models.Model.save=save #修改save方法










