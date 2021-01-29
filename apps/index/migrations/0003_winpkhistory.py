# Generated by Django 2.2.5 on 2020-11-26 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_userloginbuildingrecord'),
        ('index', '0002_answer_catgrage_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinPKHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_classfiy', models.SmallIntegerField(choices=[(1, '轮播图'), (2, '首页广告位'), (3, '详情页广告位')], default=0, verbose_name='类型')),
                ('building_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='准备上楼盘详情页的id')),
                ('price', models.IntegerField(blank=True, default=0, null=True, verbose_name='成交金额')),
                ('create_time', models.DateField(auto_now_add=True, null=True, verbose_name='数据创建时间')),
                ('fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authorization.MiddlePeople', verbose_name='顾问')),
            ],
            options={
                'verbose_name': '成功竞价记录',
                'verbose_name_plural': '成功竞价记录',
                'db_table': 'tb_win_pk_history',
                'managed': True,
            },
        ),
    ]