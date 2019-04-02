from django.contrib import admin
from .models import Questions,Choice,Mymodel
# Register your models here.
admin.site.register(Questions)
admin.site.register(Choice)
admin.site.register(Mymodel)