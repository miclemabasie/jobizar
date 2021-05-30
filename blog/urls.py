from django.urls import path
from .feeds import LatestPostsFeed
from .views import (
    post_list,
    post_detail,
    PostListView,
    share_post,
    add_comment,
    search,
)

app_name = 'blog'


urlpatterns = [
    path('', post_list, name='post-list'),
    # list of posts with tags
    path('tag/post-list/<slug:tag_slug>/', post_list, name='tag-post-list'),
    path('post-detail/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post_detail, name='post-detail'),
    path('list/', PostListView.as_view(), name='list'),
    path('tag-list/<slug>/', PostListView.as_view(), name='tag-post-listview'),
    path('share-post/<int:post_id>/', share_post, name='share-post'),
    path('add-comment/<int:post_id>/', add_comment, name='add-comment'),
    path('feed/', LatestPostsFeed(), name='post-feed'),
    path('search-post/', search, name='search-post')
]
