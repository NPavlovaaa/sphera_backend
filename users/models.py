from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.CharField(primary_key=True, unique=True, max_length=200)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    # first_name = models.CharField(max_length=100, null=True, blank=True)
    # last_name = models.CharField(max_length=100, null=True, blank=True)
    # email = models.CharField(unique=True, max_length=150, null=True, blank=True)
    # phone = models.CharField(unique=True, null=True, blank=True, max_length=11)
    # avatar = models.ImageField(upload_to='images/', null=True)
    # birthday = models.DateField(null=True)
    # level = models.ForeignKey('Level', models.DO_NOTHING)
    # scores = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'





