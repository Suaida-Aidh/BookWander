# Generated by Django 4.2.6 on 2023-10-30 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]
