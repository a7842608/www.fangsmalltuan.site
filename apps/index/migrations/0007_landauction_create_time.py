# Generated by Django 2.2.5 on 2020-11-28 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_auto_20201127_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='landauction',
            name='create_time',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
    ]
