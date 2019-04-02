from django.db import models

# Create your models here.
class Questions(models.Model):
    name=models.CharField('提问者',max_length=500)
    views=models.IntegerField('问题',default=0)
    created=models.DateTimeField(verbose_name='创建时间',auto_now_add=True,blank=False,null=False)
    edit=models.DateField(auto_now=True)

    def __str__(self):
        return "%s"%self.name

class Choice(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    content=models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "%s"%self.content

class Mymodel(models.Model):
    username=models.CharField(max_length=200)