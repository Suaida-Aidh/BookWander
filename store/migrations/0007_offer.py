# Generated by Django 4.2.6 on 2023-11-25 03:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_coupon_product_product_coupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=50, null=True)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
