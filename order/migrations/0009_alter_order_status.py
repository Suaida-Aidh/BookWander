# Generated by Django 4.2.5 on 2024-02-20 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]