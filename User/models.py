from django.db import models
from django.contrib.auth.models import AbstractUser

def RandomString():
    from Config.Tools import RandomString as R
    return R(35)

class User(AbstractUser):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=300)
    key = models.CharField(max_length=35,default=RandomString,unique=True)
