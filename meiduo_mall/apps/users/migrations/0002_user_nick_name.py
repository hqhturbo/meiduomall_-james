# Generated by Django 2.2 on 2021-11-04 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nick_name',
            field=models.CharField(default='未知用户', max_length=20),
        ),
    ]
