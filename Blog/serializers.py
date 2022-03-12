from rest_framework import serializers
from .models import Post, Category, Tag, Comment, SavePost
import datetime


class SerializerTag(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'slug': instance.getSlug(),
            'title': instance.title
        }


class SerializerDateTimePublish(serializers.DateTimeField):
    def to_representation(self, value):
        return datetime.datetime(value.year, value.month, value.hour).strftime('%b %d, %Y')


class SeralizerCategoryRelated(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'slug': value.getSlug(),
            'title': value.title
        }


class SeralizerCategory(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'slug': instance.getSlug(),
            'title': instance.title,
            'countPosts': instance.getCountPosts()
        }


class SerializerTagsRelated(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'slug': value.getSlug(),
            'title': value.title
        }


class SerializerComment(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'name': instance.name,
            'message': instance.message,
            'timePast': instance.getTimePast(),
            'profile': instance.imageProfile,
            'replied': instance.replied,
        }
        if instance.replied_comment:
            data['replied_comment'] = {}
            data['replied_comment']['id'] = instance.replied_comment.id
            data['replied_comment']['name'] = instance.replied_comment.name
        return data


class SerializerPostList(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source='getSlug')
    dateTimePublish = serializers.CharField(source='getTimePastPublished')
    urlCover = serializers.ReadOnlyField(source='getUrlCover')
    withVideo = serializers.ReadOnlyField(source='stateWithVideo')
    commentsCount = serializers.ReadOnlyField(source='getCommentsCount')
    category = SeralizerCategoryRelated(read_only=True)

    class Meta:
        model = Post
        exclude = ['published', 'tags']


class SerializerPostDetail(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source='getSlug')
    timePast = serializers.CharField(source='getTimePastPublished')
    urlCover = serializers.ReadOnlyField(source='getUrlCover')
    urlVideo = serializers.ReadOnlyField(source='getUrlVideo')
    withVideo = serializers.ReadOnlyField(source='stateWithVideo')
    comments = SerializerComment(source='getComments', many=True)
    commentsCount = serializers.ReadOnlyField(source='getCommentsCount')
    relatedPosts = SerializerPostList(source='getRelatedPosts', many=True)
    category = SeralizerCategoryRelated(read_only=True)
    tags = SerializerTagsRelated(read_only=True, many=True)
    likesCount = serializers.ReadOnlyField(source='getLikesCount')

    class Meta:
        model = Post
        exclude = ['published']


class SerializerPostSaved(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source='post.getSlug')
    dateTimePublish = serializers.CharField(source='post.getTimePastPublished')
    urlCover = serializers.ReadOnlyField(source='post.getUrlCover')
    withVideo = serializers.ReadOnlyField(source='post.stateWithVideo')
    commentsCount = serializers.ReadOnlyField(source='post.getCommentsCount')
    category = SeralizerCategoryRelated(read_only=True)

    class Meta:
        model = SavePost
        fields = '__all__'




class SerializerPostDetailLink(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source='getSlug')

    class Meta:
        model = Post
        fields = ['title', 'slug']


class SerializerPagePagination(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'has_previous': instance.has_previous(),
            'has_next': instance.has_next()
        }


class SerializerPagination(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'currentPage': instance.currentPage,
            'lastPage': instance.lastPage,
            'listRange': instance.listRange,
            'countPages': instance.countPages,
            'num_pages': instance.num_pages
        }
