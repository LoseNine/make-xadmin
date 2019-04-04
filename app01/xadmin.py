from xadmin.service.xadmin import site,ModelXadmin
from .models import Publish,Author,Book
from django.utils.safestring import mark_safe

# class QuestionConfig(ModelXadmin):
#     #自定义的config
#     def Edit(self,obj=None):
#         model_name=self.model._meta.model_name
#         app_label=self.model._meta.app_label
#         return mark_safe("<a href='/xadmin/{}/{}/{}/edit' id='edit'>编辑</a>".format(app_label,model_name,obj.pk))
#
#
#     def Del(self,obj=None):
#         model_name=self.model._meta.model_name
#         app_label=self.model._meta.app_label
#         return mark_safe("<a href='/xadmin/{}/{}/{}/delete' >删除</a>".format(app_label,model_name,obj.pk))
#
#     def Check(self,obj=None):
#         return mark_safe("<input type='checkbox'>")
#
#     list_display=[Check,"id","name",'views','created',Edit,Del]


site.register(Publish)
site.register(Book)
site.register(Author)
