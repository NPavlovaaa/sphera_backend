from django.db import models
from clients.models import Client


# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_text = models.TextField()
    review_date = models.DateField()
    delivery_assessment = models.IntegerField()
    product_quality_assessment = models.IntegerField()
    client = models.ForeignKey(Client, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reviews'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField()
    comment_date = models.DateField()
    review = models.ForeignKey('Review', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments'
