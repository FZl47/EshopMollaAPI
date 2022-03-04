from django.contrib import admin
from django.db import models
from .models import Post, Category, Tag
from django import forms

#
# class CustomeAdminModelPost(admin.ModelAdmin):
#     formfield_overrides = {
#         models.FileField:{
#             'widget':forms.FileInput(attrs={'accept':'video/mp4'})
#         }
#     }
#

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
