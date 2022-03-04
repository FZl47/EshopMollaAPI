from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.decorators import api_view
from .serializers import SerializerPostList, SeralizerCategory, SerializerTag
from .models import Post, Category, Tag
import datetime


def _get_categories():
    return SeralizerCategory(Category.objects.all(), many=True).data


def _get_tags():
    return SerializerTag(Tag.objects.all(), many=True).data


def _get_popular_posts():
    return SerializerPostList(Post.objects.getPopular(),many=True).data


@api_view(['POST'])
def get_posts(request):
    posts = Post.objects.getPost()
    try:
        posts = SerializerPostList(posts, many=True).data
    except:
        posts = SerializerPostList(posts, many=False).data
    response = {
        'Posts': posts,
        'Categories': _get_categories(),
        'Tags': _get_tags(),
        'PopularPosts': _get_popular_posts(),
    }
    return Response(response)

@api_view(['POST'])
def get_posts_by_search(request):
    data = request.POST
    searchValue = data.get('search') or None
    if searchValue:
        posts = Post.objects.getPostBySearch(searchValue)
        posts = SerializerPostList(posts, many=True).data
        response = {
            'Posts': posts,
            'Categories': _get_categories(),
            'Tags': _get_tags(),
            'PopularPosts': _get_popular_posts(),
        }
        return Response(response)
    return []


@api_view(['POST'])
def get_posts_by_category(request, slug):
    posts = Post.objects.getPostByCategory(slug)
    category = Category.objects.getBySlug(slug)
    try:
        posts = SerializerPostList(posts, many=True).data
    except:
        posts = SerializerPostList(posts, many=False).data
    response = {
        'Posts': posts,
        'Category': SeralizerCategory(category, many=False).data,
        'Categories': _get_categories(),
        'Tags': _get_tags(),
        'PopularPosts': _get_popular_posts(),
    }
    return Response(response)


@api_view(['POST'])
def get_posts_by_tag(request, slug):
    posts = Post.objects.getPostByTag(slug)
    tag = Tag.objects.getBySlug(slug)
    try:
        posts = SerializerPostList(posts, many=True).data
    except:
        posts = SerializerPostList(posts, many=False).data
    response = {
        'Posts': posts,
        'Tag': SerializerTag(tag, many=False).data,
        'Tags': _get_tags(),
        'Categories': _get_categories(),
        'PopularPosts': _get_popular_posts(),
    }
    return Response(response)



@api_view(['POST'])
def get_tags(request):
    return Response({'Tags':_get_tags()})

@api_view(['POST'])
def get_categories(request):
    return Response({'Categories':_get_categories()})

@api_view(['POST'])
def get_popular_posts(request):
    return Response({'PopularPosts':_get_popular_posts()})