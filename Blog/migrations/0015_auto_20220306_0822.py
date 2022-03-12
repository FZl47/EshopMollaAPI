# Generated by Django 3.2 on 2022-03-06 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0014_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='replied',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='replied_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Blog.comment'),
        ),
    ]
