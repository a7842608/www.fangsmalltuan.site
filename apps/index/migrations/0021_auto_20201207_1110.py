# Generated by Django 2.2.5 on 2020-12-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0020_auto_20201206_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onehouseoneprice',
            name='all_price',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='总价'),
        ),
        migrations.AlterField(
            model_name='onehouseoneprice',
            name='gave_house',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='得房率'),
        ),
        migrations.AlterField(
            model_name='onehouseoneprice',
            name='one_price',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='单价'),
        ),
    ]