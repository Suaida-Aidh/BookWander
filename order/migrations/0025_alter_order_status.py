# Generated by Django 4.2.6 on 2023-11-25 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Out For Shipping', 'Out For Shipping'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]
