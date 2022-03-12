from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from .models import Post, Category, Tag, SavePost, LikePost, Comment
from django.core.paginator import Paginator
from Config.Tools import ValidationText, ValidationEmail
from .permissions import IsAuthenticated
import datetime
import json
import math


def getObjectsPagination(req, listObjects):
    step = 4  # How many products to display

    def noneVal():
        pagination = Paginator([], step)
        pagination.currentPage = 1
        pagination.step = step
        getPage = pagination.get_page(1)
        getPage = SerializerPagePagination(getPage).data
        return [], getPage, pagination

    numberPage = req.data.get('PAGE') or 1
    pagination = Paginator(listObjects, step)
    try:
        numberPage = int(numberPage)
        if numberPage < 1:
            numberPage = 1
        pagination.currentPage = numberPage
        pagination.step = step
        pagination.countPages = int(math.ceil((len(listObjects) / step)))
        pagination.lastPage = pagination.countPages
        listRange = []
        if numberPage - 1 > 1:
            listRange.append(numberPage - 1)
        for i in range(numberPage, numberPage + 3):
            if i < pagination.lastPage and i > 1:
                listRange.append(i)
        pagination.listRange = listRange
    except:
        return noneVal()
    if numberPage <= pagination.num_pages:
        getPage = pagination.get_page(numberPage)
        objects_list = getPage.object_list
        getPage = SerializerPagePagination(getPage).data
        pagination = SerializerPagination(pagination).data
        return objects_list, getPage, pagination
    return noneVal()


def _get_categories():
    return SeralizerCategory(Category.objects.all(), many=True).data


def _get_tags():
    return SerializerTag(Tag.objects.all(), many=True).data


def _get_popular_posts():
    return SerializerPostList(Post.objects.getPopular(), many=True).data


def _get_saved_posts_id(request):
    data = request.data
    key = data.get('keyUser') or None
    if key:
        return SavePost.objects.filter(key=key).values_list('post_id', flat=True)
    return []


def _get_liked_posts(request):
    data = request.data
    key = data.get('keyUser') or None
    if key:
        return LikePost.objects.filter(key=key).values_list('post_id', flat=True)
    return []


@api_view(['POST'])
def get_posts(request):
    posts = Post.objects.getPosts()
    posts, pageActive, pagination = getObjectsPagination(request, posts)
    try:
        posts = SerializerPostList(posts, many=True).data
    except:
        posts = SerializerPostList(posts, many=False).data

    response = {
        'Posts': posts,
        'Categories': _get_categories(),
        'Tags': _get_tags(),
        'PopularPosts': _get_popular_posts(),
        'PostSavedID': _get_saved_posts_id(request),
        'pageActive': pageActive,
        'pagination': pagination
    }
    return Response(response)


@api_view(['POST'])
def get_post(request):
    data = request.POST
    slug = data.get('slug') or '-0'
    postID = str(slug).split('-')[-1]
    post = Post.objects.filter(id=postID).first()
    if post != None:
        nextPost = Post.objects.getNextPost(post.id)
        prevPost = Post.objects.getPrevPost(post.id)
        response = {
            'Post': SerializerPostDetail(post).data,
            'Categories': _get_categories(),
            'Tags': _get_tags(),
            'PopularPosts': _get_popular_posts(),
            'PostSavedID': _get_saved_posts_id(request),
            'PostLiked': _get_liked_posts(request),
        }
        if nextPost == None:
            response['NextPost'] = None
        else:
            response['NextPost'] = SerializerPostDetailLink(nextPost).data

        if prevPost == None:
            response['PrevPost'] = None
        else:
            response['PrevPost'] = SerializerPostDetailLink(prevPost).data

        return Response(response)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def get_posts_by_search(request):
    data = request.POST
    searchValue = data.get('search') or None
    if searchValue:
        posts = Post.objects.getPostBySearch(searchValue)
        posts, pageActive, pagination = getObjectsPagination(request, posts)
        posts = SerializerPostList(posts, many=True).data
        response = {
            'Posts': posts,
            'Categories': _get_categories(),
            'Tags': _get_tags(),
            'PopularPosts': _get_popular_posts(),
            'PostSavedID': _get_saved_posts_id(request),
            'pageActive': pageActive,
            'pagination': pagination
        }
        return Response(response)
    return []


@api_view(['POST'])
def get_posts_by_category(request, slug):
    posts = Post.objects.getPostByCategory(slug)
    category = Category.objects.getBySlug(slug)
    posts, pageActive, pagination = getObjectsPagination(request, posts)
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
        'PostSavedID': _get_saved_posts_id(request),
        'pageActive': pageActive,
        'pagination': pagination
    }
    return Response(response)


@api_view(['POST'])
def get_posts_by_tag(request, slug):
    posts = Post.objects.getPostByTag(slug)
    posts, pageActive, pagination = getObjectsPagination(request, posts)
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
        'PostSavedID': _get_saved_posts_id(request),
        'pageActive': pageActive,
        'pagination': pagination
    }
    return Response(response)


@api_view(['POST'])
def save_post(request):
    response = {}
    try:
        data = request.POST
        postID = data.get('id') or 0
        keyBlogUser = data.get('keyUser') or None
        post = Post.objects.filter(id=postID).first()
        if keyBlogUser != None and post != None:
            savePost = SavePost.objects.filter(key=keyBlogUser, post_id=post.id).first()
            if savePost != None:
                savePost.delete()
                response['status_action'] = 'delete'
            else:
                SavePost.objects.create(key=keyBlogUser, post_id=post.id)
                response['status_action'] = 'save'
            response['status_code'] = 200
            response['status_text'] = 'OK'
        else:
            response['status_code'] = 404
            response['status_text'] = 'Key or Post id is not valid'
    except:
        response['status_code'] = 500
        response['status_text'] = 'Something went wrong'
    return Response(response)


@api_view(['POST'])
def like_post(request):
    response = {}
    try:
        data = request.POST
        postID = data.get('id') or 0
        keyBlogUser = data.get('keyUser') or None
        post = Post.objects.filter(id=postID).first()
        if keyBlogUser != None and post != None:
            likePost = LikePost.objects.filter(key=keyBlogUser, post_id=post.id).first()
            if likePost != None:
                likePost.delete()
                response['status_action'] = 'unlike'
            else:
                LikePost.objects.create(key=keyBlogUser, post_id=post.id)
                response['status_action'] = 'like'
            response['status_code'] = 200
            response['status_text'] = 'OK'
        else:
            response['status_code'] = 404
            response['status_text'] = 'Key or Post id is not valid'
    except:
        response['status_code'] = 500
        response['status_text'] = 'Something went wrong'
    return Response(response)


@api_view(['POST'])
def comment_post(request):
    response = {}
    data = request.data
    name = data.get('name') or None
    email = data.get('email') or None
    message = data.get('message') or None
    postID = data.get('postID') or 0
    keyUser = data.get('keyUser') or None
    replied = data.get('replied') or False
    replied_comment = data.get('replied_comment') or 0
    if ValidationText(name, 2, 51) and ValidationEmail(email, 2, 101) and ValidationText(message, 2,
                                                                                         1001) and keyUser and postID:
        post = Post.objects.filter(id=postID).first()
        if post != None:
            if replied == 'True' or replied == True:
                replied_comment = Comment.objects.filter(id=replied_comment).first()
                if replied_comment != None:
                    Comment.objects.create(name=name, email=email, message=message, post_id=post.id, key=keyUser,
                                           replied=True, replied_comment_id=replied_comment.id)
                    response['status_text'] = 'OK'
                    response['status_code'] = 200
                else:
                    response['status_text'] = 'Reply comment not found'
                    status_code = 404
                    response['status_code'] = 404
            else:
                Comment.objects.create(name=name, email=email, message=message, post_id=post.id, key=keyUser)
                response['status_text'] = 'OK'
                response['status_code'] = 200
        else:
            response['status_text'] = 'Post not found'
            response['status_code'] = 404
    else:
        response['status_text'] = 'Please fill the fields correctly'
        response['status_code'] = 204
    return Response(response)


@api_view(['POST'])
def get_tags(request):
    return Response({'Tags': _get_tags()})


@api_view(['POST'])
def get_categories(request):
    return Response({'Categories': _get_categories()})


@api_view(['POST'])
def get_popular_posts(request):
    return Response({'PopularPosts': _get_popular_posts()})


@api_view(['POST'])
def get_saved_posts(request):
    data = request.data
    key = data.get('keyUser') or None
    if key:
        saved_post = SavePost.objects.filter(key=key).all()
        saved_post = [i.post for i in saved_post]
        saved_post = SerializerPostList(saved_post, many=True).data
        response = {
            'Posts': saved_post,
            'Tags': _get_tags(),
            'Categories': _get_categories(),
            'PopularPosts': _get_popular_posts(),
            'PostSavedID': _get_saved_posts_id(request),
        }
        return Response(response)
    return []
