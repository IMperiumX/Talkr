# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Profile, Post, PostReaction, Retalk, PostView, Comment, Contact


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'date_of_birth',
        'bio',
        'photo',
        'background_image',
        'is_active',
        'user',
    )
    list_filter = (
        'created',
        'modified',
        'date_of_birth',
        'is_active',
        'user',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'body',
        'media',
        'total_likes',
        'status',
        'type',
        'published',
        'is_private',
        'author',
    )
    list_filter = (
        'created',
        'modified',
        'published',
        'is_private',
        'author',
    )
    raw_id_fields = ('liked_users', 'tags')


@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'type', 'user', 'post')
    list_filter = ('created', 'modified', 'user', 'post')


@admin.register(Retalk)
class RetalkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'original_post',
        'retalked_by',
        'retalk',
    )
    list_filter = ('created_at', 'original_post', 'retalked_by', 'retalk')
    date_hierarchy = 'created_at'


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'post')
    list_filter = ('created_at', 'post')
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'body',
        'media',
        'user',
        'post',
    )
    list_filter = ('created', 'modified', 'user', 'post')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user_from', 'user_to')
    list_filter = ('created', 'user_from', 'user_to')
