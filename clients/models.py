from django.db import models

from products.models import Product, WeightSelection
from users.models import User
from orders.models import Order

class Client(models.Model):
    def upload_to(instance, filename):
        return 'avatars/{filename}'.format(filename=filename)

    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(unique=True, max_length=11)
    user = models.ForeignKey(User, models.DO_NOTHING)
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
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
    weight_selection = models.ForeignKey(WeightSelection, models.DO_NOTHING)
    product_count = models.IntegerField(null=True)
    client = models.ForeignKey('Client', models.DO_NOTHING)
    order = models.ForeignKey(Order, models.DO_NOTHING, null=True)
    active = models.BooleanField(null=True, blank=True)

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


