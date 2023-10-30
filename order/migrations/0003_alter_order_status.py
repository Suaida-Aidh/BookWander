# Generated by Django 4.2.6 on 2023-10-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]