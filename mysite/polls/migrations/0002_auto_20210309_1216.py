# Generated by Django 3.1.7 on 2021-03-09 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.IntegerField(default=0),
        ),
    ]
