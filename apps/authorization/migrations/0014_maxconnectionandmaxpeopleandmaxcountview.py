# Generated by Django 2.2.5 on 2020-12-02 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0013_sensitiveword_if_talk'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaxConnectionAndMaxPeopleAndMaxCountView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now=True, verbose_name='数据创建时间')),
                ('chat_second', models.CharField(blank=True, max_length=255, null=True, verbose_name='聊天限制时间/秒数')),
                ('chat_people', models.CharField(blank=True, max_length=255, null=True, verbose_name='最大人数')),
                ('chat_count', models.CharField(blank=True, max_length=255, null=True, verbose_name='最大聊天次数')),
            ],
            options={
                'verbose_name': '聊天人数上限, 聊天次数, 限制时间',
                'verbose_name_plural': '聊天人数上限, 聊天次数, 限制时间',
                'db_table': 'tb_chat_connection',
                'managed': True,
            },
        ),
    ]
