from django.contrib import admin

from posts.models import Group, Post
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
