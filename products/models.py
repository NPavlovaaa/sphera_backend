from django.db import models

from users.models import User


class Product(models.Model):
    def upload_to(self, filename):
        return 'product_images/{filename}'.format(filename=filename)

    product_id = models.AutoField(primary_key=True)
    product_description = models.CharField(max_length=2000, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', models.DO_NOTHING)
    roasting_method = models.ForeignKey('RoastingMethod', models.DO_NOTHING)
    taste = models.CharField(max_length=200, blank=True, null=True)
    processing_method = models.ForeignKey('ProcessingMethod', models.DO_NOTHING)
    quantity = models.IntegerField()
    acidity = models.IntegerField()
    density = models.IntegerField()
    sweetness = models.IntegerField()
    bitterness = models.IntegerField()
    rating = models.FloatField()
    image_min = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image_max = models.ImageField(upload_to=upload_to, blank=True, null=True)
    base_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'products'


class Variety(models.Model):
    variety_id = models.AutoField(primary_key=True)
    variety_name = models.CharField(max_length=30)
    variety_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'varieties'


class ProductVariety(models.Model):
    product_variety_id = models.AutoField(primary_key=True)
    variety = models.ForeignKey('Variety', models.DO_NOTHING)
    product = models.ForeignKey('Product', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product_variety'


class RoastingMethod(models.Model):
    roasting_method_id = models.AutoField(primary_key=True)
    roasting_method_name = models.CharField(max_length=500)
    roasting_method_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roasting_methods'


class ProcessingMethod(models.Model):
    processing_method_id = models.AutoField(primary_key=True)
    processing_method_name = models.CharField(max_length=30)
    processing_method_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'processing_methods'


class Category(models.Model):
    def upload_to(self, filename):
        return 'category_images/{filename}'.format(filename=filename)

    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)
    category_description = models.TextField(blank=True, null=True)
    note = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Weight(models.Model):
    weight_id = models.AutoField(primary_key=True)
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'weight'


class WeightSelection(models.Model):
    weight_selection_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    weight = models.ForeignKey('Weight', models.DO_NOTHING)
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'weight_selection'


class MakingMethod(models.Model):
    def upload_to(self, filename):
        return 'making_methods/{filename}'.format(filename=filename)

    making_method_id = models.AutoField(primary_key=True)
    making_method_name = models.CharField(max_length=100)
    making_method_description = models.TextField(max_length=3000, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to)

    class Meta:
        managed = False
        db_table = 'making_methods'


class ProductMakingMethod(models.Model):
    product_making_method_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    making_method = models.ForeignKey('MakingMethod', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product_making_methods'


class AdminProductChange(models.Model):
    admin_product_change_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    count = models.IntegerField()
    action = models.CharField(max_length=100)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'admin_product_changes'
