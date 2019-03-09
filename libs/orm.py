


class ModelMixin:
    def to_dict(self,*exclude):
        #将model对象转换为属性字典  exclude 需要排除的字段
        attr_dict={}
        for field in  self._meta.fields:
            field_name=field.attname
            if field_name not in exclude:
                attr_dict[field_name]=getattr(self,field_name)
        return attr_dict















