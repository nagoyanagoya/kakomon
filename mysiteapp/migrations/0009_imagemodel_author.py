# Generated by Django 2.2.12 on 2020-05-09 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysiteapp', '0008_auto_20200509_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='author',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
