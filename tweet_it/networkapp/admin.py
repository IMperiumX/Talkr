from django.contrib import admin

from .models import Contact, Post, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date_of_birth", "photo", "is_active")
    list_filter = ("user", "date_of_birth", "is_active")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "body",
        "date_added",
        "publish",
        "status",
        "total_likes",
    )
    list_filter = ("author", "date_added", "publish")
    raw_id_fields = ("users_like",)
    search_fields = ("title", "body", "author")
    date_hierarchy = "publish"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "user_from", "user_to", "created")
    list_filter = ("user_from", "user_to", "created")
