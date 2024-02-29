# Generated by Django 4.2.5 on 2024-02-28 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out For Shipping', 'Out For Shipping'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]