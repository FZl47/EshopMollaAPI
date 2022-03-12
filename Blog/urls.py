from django.urls import path
from . import views

app_name = 'Blog'
urlpatterns = [
    path('get-post',views.get_post),
    path('get-posts',views.get_posts),
    path('post/save',views.save_post),
    path('post/like',views.like_post),
    path('post/comment',views.comment_post),
    path('get-posts/search',views.get_posts_by_search),
    path('get-posts-by-category/<str:slug>',views.get_posts_by_category),
    path('get-posts-by-tag/<str:slug>',views.get_posts_by_tag),
    path('get-tags/',views.get_tags),
    path('get-categories/',views.get_categories),
    path('get-popular-posts/',views.get_popular_posts),
    path('get-saved-posts/',views.get_saved_posts),
]