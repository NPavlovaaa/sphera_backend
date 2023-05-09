from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def upload_to(self, filename):
        return 'avatars/{filename}'.format(filename=filename)

    user_id = models.CharField(primary_key=True, unique=True, max_length=200)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    role = models.ForeignKey('Role', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'roles'



