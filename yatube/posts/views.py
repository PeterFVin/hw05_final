from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from core.utils import paginate
from posts.forms import CommentForm, PostForm
from posts.models import Follow, Group, Post, User


@cache_page(20)
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'posts/index.html',
        paginate(
            request=request,
            queryset=Post.objects.select_related('author', 'group'),
        ),
    )


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    return render(
        request,
        'posts/group_list.html',
        {
            'group': group,
            **paginate(
                request=request,
                queryset=Post.objects.filter(group=group).select_related(
                    'group',
                ),
            ),
        },
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    author = get_object_or_404(User, username=username)
    following = (
        request.user.is_authenticated
        and request.user != author
        and author.following.filter(user=request.user, author=author).exists()
    )
    return render(
        request,
        'posts/profile.html',
        {
            'author': author,
            'following': following,
            **paginate(
                request=request,
                queryset=author.posts.select_related('group', 'author'),
            ),
        },
    )


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None)
    return render(
        request,
        'posts/post_detail.html',
        {'post': post, 'form': form},
    )


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(reverse('posts:post_detail', kwargs={'pk': pk}))


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {'form': form},
        )
    form.instance.author = request.user
    form.save()
    return redirect('posts:profile', request.user)


@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
    return redirect('posts:post_detail', pk)

    return render(
        request,
        'posts/create_post.html',
        {
            'post': post,
            'form': form,
            'is_edit': True,
        },
    )


@login_required
def follow_index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'posts/follow.html',
        paginate(
            request=request,
            queryset=Post.objects.filter(author__following__user=request.user),
        ),
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    follow = get_object_or_404(User, author__username=request.user)
    follow.delete()
    return redirect('posts:profile', username=username)
