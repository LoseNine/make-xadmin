from django.contrib import admin
from .models import Publish,Author,Book
# Register your models here.
admin.site.register(Publish)
admin.site.register(Author)
admin.site.register(Book)