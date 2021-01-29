# Generated by Django 2.2.5 on 2020-11-26 10:25

from django.db import migrations, models
import django.db.models.deletion
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0003_userloginrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLoginBuildingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, null=True, verbose_name='数据创建时间')),
                ('user_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='用户名')),
                ('header_img', utils.fields.QiniuField(blank=True, max_length=500, null=True, verbose_name='头像')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authorization.Users', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '用户访问楼盘记录',
                'verbose_name_plural': '用户访问楼盘记录',
                'db_table': 'tb_user_login_building_record',
                'managed': True,
            },
        ),
    ]