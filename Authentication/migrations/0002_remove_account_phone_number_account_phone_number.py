# Generated by Django 4.2.6 on 2023-10-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='Phone_number',
        ),
        migrations.AddField(
            model_name='account',
            name='phone_number',
            field=models.CharField(default=False, max_length=20),
        ),
    ]
