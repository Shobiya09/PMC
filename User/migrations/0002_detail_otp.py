# Generated by Django 3.1.7 on 2021-04-07 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='otp',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
