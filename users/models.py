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


class AdminIncomeChange(models.Model):
    admin_income_change_id = models.AutoField(primary_key=True)
    note = models.TextField(max_length=500)
    user = models.ForeignKey(User, models.DO_NOTHING)
    action = models.CharField(max_length=100)
    date = models.DateField()
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_income_changes'
