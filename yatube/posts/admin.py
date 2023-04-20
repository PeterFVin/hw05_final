from django.contrib import admin

from posts.models import Comment, Follow, Group, Post
from yatube.admin import BaseAdmin


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    fields = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )


@admin.register(Group)
class GroupAdmin(BaseAdmin):
    list_display = (
        'pk',
        'title',
        'slug',
        'description',
    )
    search_fields = ('title',)
    fields = (
        'pk',
        'title',
        'slug',
        'description',
    )


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    list_display = (
        'pk',
        'post',
        'text',
        'author',
        'created',
    )
    search_fields = (
        'post',
        'text',
    )
    fields = (
        'pk',
        'post',
        'text',
        'author',
        'created',
    )


@admin.register(Follow)
class FollowAdmin(BaseAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = (
        'user',
        'author',
    )
    fields = (
        'pk',
        'user',
        'author',
    )
