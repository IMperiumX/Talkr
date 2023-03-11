from django.urls import path

from tweet_it.networkapp.views import (
    create_post,
    following_posts,
    like,
    post_delete_view,
    post_detail_view,
    post_list_view,
    post_update_view,
    user_detail_view,
    user_follow,
    user_list_view,
)

app_name = "networkapp"

urlpatterns = [
    # AUTH URLs
    # Post related URLs
    path("", post_list_view, name="index"),
    path("like/", like, name="like"),
    path("post/new", create_post, name="post_new"),
    path("post/<int:pk>/", post_detail_view, name="post_detail"),
    path("post/<int:pk>/edit/", post_update_view, name="post_edit"),
    path("post/<int:pk>/delete/", post_delete_view, name="post_delete"),
    # User action realted URLs
    path("edit/", post_update_view, name="edit"),
    path("users/follow/", user_follow, name="user_follow"),
    path("users/", user_list_view, name="user_list"),
    path("users/<username>/following/", following_posts, name="user_following"),
    path(
        "users/<username>/",
        user_detail_view,
        name="user_detail",
    ),
]
