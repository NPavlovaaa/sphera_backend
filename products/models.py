from django.db import models


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_description = models.CharField(max_length=500, blank=True, null=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', models.DO_NOTHING)
    roasting_method = models.ForeignKey('RoastingMethod', models.DO_NOTHING)
    variety = models.ForeignKey('Variety', models.DO_NOTHING)
    taste = models.CharField(max_length=200, blank=True, null=True)
    processing_method = models.ForeignKey('ProcessingMethod', models.DO_NOTHING)
    quantity = models.IntegerField()

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


class RoastingMethod(models.Model):
    roasting_method_id = models.AutoField(primary_key=True)
    roasting_method_name = models.CharField(max_length=30)
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
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)
    category_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Weight(models.Model):
    weight_id = models.AutoField(primary_key=True)
    weight = models.CharField(max_length=150)

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


