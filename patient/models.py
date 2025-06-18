from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class Pacient(AbstractBaseUser):
    bio = models.TextField(max_length=16000)
    


