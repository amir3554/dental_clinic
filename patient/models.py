from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Patient(AbstractUser):
    email = models.EmailField('email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    bio = models.TextField(max_length=1600)

    def __str__(self):
        return self.first_name + ' ' + self.first_name
    
    class Meta:
            db_table = 'patient'  # Optional: Custom table name

