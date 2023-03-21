from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.CharField(primary_key=True, unique=True, max_length=200)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(unique=True, max_length=150, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'users'





