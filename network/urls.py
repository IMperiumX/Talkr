from django.urls import path

from . import views

urlpatterns = [
    # AUTH URLs
    # Post related URLs
    path("", views.post_list_view, name="index"),
    path("like/", views.like, name="like"),
    path("post/new", views.create_post, name="post_new"),
    path("post/<int:pk>/", views.post_detail_view, name="post_detail"),
    path("post/<int:pk>/edit/", views.post_update_view, name="post_edit"),
    path("post/<int:pk>/delete/", views.post_delete_view, name="post_delete"),
    # User action realted URLs
    path("edit/", views.post_update_view, name="edit"),
    path("users/follow/", views.user_follow, name="user_follow"),
    path("users/", views.user_list_view, name="user_list"),
    path("users/<username>/following/", views.following_posts, name="user_following"),
    path(
        "users/<username>/",
        views.user_detail_view,
        name="user_detail",
    ),
]
