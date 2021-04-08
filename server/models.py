from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class story(models.Model):
  headline = models.TextField(max_length=64)
  category = models.CharField(max_length=6)
  region = models.CharField(max_length=2)
  author = models.ForeignKey('authors', on_delete=models.CASCADE)
  date = models.DateField(auto_now_add=True)
  details = models.TextField(max_length=512)

  def __str__(self):
    return self.headline


class authors(models.Model):
  #user=models.OneToOneField(User,unique=True,verbose_name='user',on_delete=models.CASCADE,default=None)
  name = models.CharField(max_length=16)
  username=models.CharField(max_length=16,unique=True,default=None)
  password=models.CharField(max_length=16,default=None)

  def __str__(self):
    return self.name
