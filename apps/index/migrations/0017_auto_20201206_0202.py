# Generated by Django 2.2.5 on 2020-12-06 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_auto_20201203_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotteryresult',
            name='pid',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='PID'),
        ),
        migrations.AddField(
            model_name='toldpurpose',
            name='pid',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='PID'),
        ),
        migrations.CreateModel(
            name='UnionLotteryResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(blank=True, max_length=500, null=True, verbose_name='PID')),
                ('building_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='楼盘名称')),
                ('create_time', models.DateTimeField(auto_now=True, null=True, verbose_name='创建时间')),
                ('fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='index.BuildingDetial', verbose_name='楼盘')),
            ],
            options={
                'verbose_name': '购房登记号顺序表(摇号结果)',
                'verbose_name_plural': '购房登记号顺序表(摇号结果)',
                'db_table': 'tb_union_lottery_result',
                'managed': True,
            },
        ),
    ]
