# Generated by Django 4.2.5 on 2024-02-27 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Out For Shipping', 'Out For Shipping'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending', max_length=150),
        ),
    ]