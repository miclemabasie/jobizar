from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres import search
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, View
from .forms import EmailPostForm, CreateCommentForm, SearchForm
from django.core.mail import send_mail

from taggit.models import Tag
from django.db.models import Count
from collections import namedtuple

def post_list(request,tag_slug=None):

    page = request.GET.get('page', 1)
    object_list = Post.published.filter()
    
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        
    template_name = 'post-list.html'
    
    context = {
        'tag': tag,
        'page': page,
        'posts': posts,
    }
    print(page)
    return render(request, template_name, context)

class PostListView(ListView):
    template_name = 'post-list.html'
    paginate_by = 3
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        queryset = Post.published.all()
        tag = None
        print(args, kwargs)
        try:
            tag = get_object_or_404(Tag, slug='programming')
            queryset = queryset.filter(tags__name=self.kwargs['slug'])
        except:
            queryset = queryset
            print('not working')
        
        return queryset

    def get_context_data(self, **kwargs):
        try:
            tag = self.kwargs['slug']
        except:
            tag = None
        context = super().get_context_data(**kwargs)
        context.update({
            'tag': tag,
        })
        print(f" this is the slug from the context {context['tag']}")
        return context
    

# Getting the detail post by slug, day, month, year

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    tags = post.tags.all()
    new_comment = None
    if request.method == 'POST':
        form = CreateCommentForm(request.POST or None)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            print(form.errors)
    else:
        form = CreateCommentForm()
    # Get the ids for all the tags related to this post
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Get all post with same tags
    similar_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # annotate posts
    similar_post = similar_post.annotate(same_tags=Count('tags'))
    similar_post = similar_post.order_by('-same_tags', '-publish')

    print(f"this are the similar post {similar_post} ")
    template_name = 'post-detail.html'

    comments = Comment.objects.filter(post=post)
    comments_count = comments.count()
    context = {
        'post': post,
        'comments': comments,
        'comments_count': comments_count,
        'form': form,
        'new_comment': new_comment,
        'tags': tags,
        'similar_post': similar_post,
    }

    return render(request, template_name, context)

def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            subject = 'Shared A Post'
            from_email = 'joberdesk@gmail.com'
            recip_list = cd['to_email']
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = f"Read {post.title} at {post_url} \n\n {cd['name']}\'s comments: {cd['comments']}" 

            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=(recip_list, ))
            sent = True
     
        else:
            print(form.errors)
    else:
        form = EmailPostForm()

    template_name = 'share-post.html'
    context = {
        'form': form,
        'post': post,
        'sent': sent
    }
    return render(request, template_name, context)


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreateCommentForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.save()
            return redirect(f'/blog/post-detail/{post.publish.year}/{post.publish.month}/{post.publish.day}/{post.slug}/')
        else:
            print(form.errors)
    else:
        form = CreateCommentForm()
        print(post.publish.day)

    template_name = 'post-detail.html'
    context = {
        'form': form,
    }
    return render(request, template_name, context)
    

def search(request):
    query = None
    results = []
    search_param = False

    if 'query' in request.GET:
        query = request.GET.get('query')
        # search_query = SearchQuery(query)
        # search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        # results = Post.published.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
        results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
        search_param = True
        print(search_param)

    context = {
      
        'query': query,
        'results': results,
        'search': search_param,
    }
    template_name = 'post-list.html'
    return render(request, template_name, context)

