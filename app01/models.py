from django.db import models

# Create your models here.
class Questions(models.Model):
    name=models.CharField(max_length=500)
    views=models.IntegerField(default=0)
    created_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Choice(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    content=models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class Mymodel(models.Model):
    username=models.CharField(max_length=200)