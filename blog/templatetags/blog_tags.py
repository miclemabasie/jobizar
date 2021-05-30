import markdown
from django import template
from ..models import Post
from django.db.models import Count
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('latest_posts.html')
def most_recent_post(count=2):
    lastest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': lastest_posts}

@register.simple_tag
def get_most_commented_post(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter
def convert_markdown(value):
    return markdown.markdown(value, extensions=['markdown.extensions.fenced_code'])