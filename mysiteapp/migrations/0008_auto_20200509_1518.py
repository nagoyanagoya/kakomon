# Generated by Django 2.2.12 on 2020-05-09 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysiteapp', '0007_auto_20200508_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='image',
            field=models.FileField(upload_to=''),
        ),
    ]