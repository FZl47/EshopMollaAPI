# Generated by Django 3.2 on 2022-03-15 20:16

import Blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0017_alter_likepost_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='imageProfile',
            field=models.CharField(default=Blog.models.RandomSrcImage, max_length=150),
        ),
    ]
