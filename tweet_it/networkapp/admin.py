from django.contrib import admin

from .models import Post, Profile

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("body", "author", "publish", "status")
    list_filter = ("date_added", "publish", "author")
    search_fields = ("title", "body", "author")
    date_hierarchy = "publish"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]
