# Generated by Django 2.2.12 on 2020-05-11 08:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysiteapp', '0010_imagemodel_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='when',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
