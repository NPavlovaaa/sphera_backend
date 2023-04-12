from django.db import models

from config import settings
from products.models import Product
from users.models import User


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(unique=True, max_length=11)
    user = models.ForeignKey(User, models.DO_NOTHING)
    avatar = models.CharField(max_length=150, blank=True, null=True)
    birthday = models.DateField(null=True)
    level = models.ForeignKey('Level', models.DO_NOTHING)
    scores = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'clients'


class Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'levels'


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, null=True)
    product_count = models.IntegerField(null=True)
    client = models.ForeignKey('Client', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'carts'


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    client = models.ForeignKey(Client, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'favorites'


