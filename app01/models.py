from django.db import models

# Create your models here.

class Author(models.Model):
    username = models.CharField('名字',max_length=200)

    def __str__(self):
        return "%s" % self.username

class Publish(models.Model):
    name=models.CharField('出版社名字',max_length=200)

    def __str__(self):
        return "%s" % self.name
    
class Book(models.Model):
    name=models.CharField('书名',max_length=500)
    publish=models.ManyToManyField(Publish)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return "%s"%self.name



