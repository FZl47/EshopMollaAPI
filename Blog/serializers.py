from rest_framework import serializers
from .models import Post, Category, Tag
import datetime


class SerializerTag(serializers.ModelSerializer):
    class Meta:
        model = Tag

    def to_representation(self, instance):
        return {
            'slug':instance.getSlug(),
            'title':instance.title
        }

class SerializerDateTimePublish(serializers.DateTimeField):
    def to_representation(self, value):
        return datetime.datetime(value.year,value.month,value.hour).strftime('%b %d, %Y')

class SeralizerCategoryRelated(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'slug':value.getSlug(),
            'title':value.title
        }

class SeralizerCategory(serializers.ModelSerializer):
    class Meta:
        model = Category,

    def to_representation(self, instance):
        return {
            'slug':instance.getSlug(),
            'title':instance.title,
            'countPosts':instance.getCountPosts()
        }

class SerializerPostList(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source='getSlug')
    dateTimePublish = serializers.CharField(source='getTimePastPublished')
    urlCover = serializers.ReadOnlyField(source='getUrlCover')
    withVideo = serializers.ReadOnlyField(source='stateWithVideo')
    comments = serializers.ReadOnlyField(source='getComments')
    commentsCount = serializers.ReadOnlyField(source='getCommentsCount')
    category = SeralizerCategoryRelated(read_only=True)

    class Meta:
        model = Post
        exclude = ['published','tags']

    
