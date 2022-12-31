from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Notes(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     title=models.CharField(max_length=200)
     description=models.TextField()

     class Meta:
         verbose_name="notes"
         verbose_name_plural="notes"

     def __str__(self):
         return self.title


class Complain(models.Model):
         email = models.EmailField(max_length=100)
         complain = models.CharField(max_length=200)
         against = models.CharField(max_length=200)
         position = models.CharField(max_length=200)
         image =  models.ImageField(upload_to = 'static', null=True, blank=True, default='2.png')
         def __str__(self) :
             return self.email 


class Comment(models.Model):
    email = models.EmailField(max_length=100)
    complain = models.ForeignKey(Complain, related_name="comments", on_delete=models.CASCADE)
    username = models.CharField(max_length=80)
    body = models.TextField(max_length=190)
    def __str__(self) :
        return self.complain.email
    
    
class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    title=models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title
