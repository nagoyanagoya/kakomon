# Generated by Django 2.2.12 on 2020-05-04 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysiteapp', '0002_subjectmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectmodel',
            name='day',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
