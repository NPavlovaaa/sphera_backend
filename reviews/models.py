from django.db import models
from clients.models import *


# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_text = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField()
    delivery_assessment = models.IntegerField()
    product_quality_assessment = models.IntegerField()
    client = models.ForeignKey(Client, models.DO_NOTHING)
    order = models.ForeignKey(Order, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reviews'

class ReviewsProduct(models.Model):
    review_product_id = models.AutoField(primary_key=True)
    review_product_text = models.TextField(null=True, blank=True)
    review_product_date = models.DateTimeField()
    product_quality_assessment = models.IntegerField()
    client = models.ForeignKey(Client, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reviews_product'

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField()
    comment_date = models.DateField()
    review = models.ForeignKey('Review', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments'
