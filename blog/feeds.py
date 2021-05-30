from django.contrib.syndication.views import Feed
from django.template.defaultfilters import  truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'Jober Desk'
    link = reverse_lazy('blog:post-list')
    description = "New Posts From JoberDesk"

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title

    def item_descrioption(self, item):
        return truncatedwords(item.body, 30)