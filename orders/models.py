from django.db import models


class DeliveryMethod(models.Model):
    def upload_to(instance, filename):
        return 'delivery_images/{filename}'.format(filename=filename)

    delivery_id = models.AutoField(primary_key=True)
    delivery_name = models.CharField(max_length=30)
    delivery_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery_methods'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_sum = models.IntegerField()
    status = models.ForeignKey('Status', models.DO_NOTHING)
    delivery = models.ForeignKey('DeliveryMethod', models.DO_NOTHING)
    order_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    dispatch_date = models.DateField(blank=True, null=True)
    package = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'orders'


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'statuses'
