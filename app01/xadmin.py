from xadmin.service.xadmin import site,ModelXadmin
from .models import Publish,Author,Book
from django.utils.safestring import mark_safe
 
class BookConfig(ModelXadmin):
     #自定义的config
     list_display=[ModelXadmin.Check,"id","name","author",'publish',ModelXadmin.Del,ModelXadmin.Edit]
     list_filter=["author","publish",'name']


site.register(Publish)
site.register(Book,BookConfig)
site.register(Author)
