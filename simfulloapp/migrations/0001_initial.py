# Generated by Django 4.0.6 on 2022-11-29 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='air',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=15)),
                ('dest', models.CharField(max_length=15)),
                ('consol', models.CharField(max_length=15)),
                ('line', models.CharField(max_length=15)),
                ('cur', models.CharField(max_length=15)),
                ('minimum', models.CharField(max_length=15)),
                ('normal', models.CharField(max_length=15)),
                ('over45', models.CharField(max_length=15)),
                ('over100', models.CharField(max_length=15)),
                ('over300', models.CharField(max_length=15)),
                ('over500', models.CharField(max_length=15)),
                ('over1000', models.CharField(max_length=15)),
                ('skdl', models.CharField(max_length=15)),
                ('fsc', models.CharField(max_length=15)),
                ('via', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='fcl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=15)),
                ('dest', models.CharField(max_length=15)),
                ('line', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=15)),
                ('cur', models.CharField(max_length=15)),
                ('rate', models.CharField(max_length=15)),
                ('unit', models.CharField(max_length=15)),
                ('chargeAt', models.CharField(max_length=15)),
                ('ttime', models.CharField(max_length=15)),
                ('vaildity', models.CharField(max_length=15)),
                ('group', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='lcl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=15)),
                ('dest', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=15)),
                ('cur', models.CharField(max_length=15)),
                ('unit', models.CharField(max_length=15)),
                ('rate', models.CharField(max_length=15)),
                ('chargeAt', models.CharField(max_length=15)),
                ('group', models.CharField(max_length=15)),
            ],
        ),
    ]
