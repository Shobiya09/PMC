# Generated by Django 3.1.7 on 2021-04-07 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_detail_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='otp',
            field=models.CharField(default='', max_length=4, unique=True),
        ),
    ]
