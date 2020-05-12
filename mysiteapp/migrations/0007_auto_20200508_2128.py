# Generated by Django 2.2.12 on 2020-05-08 12:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysiteapp', '0006_auto_20200508_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='page',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
