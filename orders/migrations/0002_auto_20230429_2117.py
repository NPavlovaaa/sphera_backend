# Generated by Django 3.2.18 on 2023-04-29 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_sum', models.IntegerField()),
                ('order_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('dispatch_date', models.DateTimeField(blank=True, null=True)),
                ('package', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]
