# Generated by Django 2.2.5 on 2020-11-26 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='catgrage_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='点评所属id'),
        ),
    ]
