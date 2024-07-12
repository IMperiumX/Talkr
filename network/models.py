from functools import partial

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel

from common.utils import file_upload
from network.constants import *
from network.managers import CommentManager, PostManager, PostReactionManager
from network.model_mixins import CommentMixin, PostMixin, PostReactionMixin
from taggit.managers import TaggableManager


class Profile(TimeStampedModel):
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(
        default="default.png",
        upload_to=partial(
            file_upload,
            "users/%Y/%m/%d/",
        ),
    )
    background_image = models.ImageField(
        upload_to=partial(file_upload, "background_images"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Profile for user {self.user.username}"

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.id)])


class Post(PostMixin, TimeStampedModel):
    STATUS = Choices(DRAFT, PUBLISHED)
    POST_TYPES = Choices(TEXT, VIDEO)

    body = models.TextField(max_length=280, null=True)
    media = models.FileField(blank=True, null=True)
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0,
    )
    status = StatusField(default=DRAFT)
    type = StatusField(choices_name="POST_TYPES", default=TEXT)
    published = MonitorField(monitor="status", when=[PUBLISHED])
    is_private = models.BooleanField(default=False)

    # relations
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="twitter_posts",
        null=True,
    )
    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True,
    )

    tags = TaggableManager()
    objects = PostManager()

    def __str__(self):
        return self.body[:50] + "..."

    class Meta:
        ordering = ("-published",)

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])


class PostReaction(PostReactionMixin, TimeStampedModel):
    REACTIONS = Choices(LIKE, LOVE, LAUGHT, SAD, CARE, ANGRY)

    type = StatusField(choices_name="REACTIONS")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="reactions",
    )

    objects = PostReactionManager()

    class Meta:
        unique_together = (("user", "post"),)

    def __str__(self):
        return f"{self.user} reacted {self.type} on {self.post}"


class Retalk(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    original_post = models.ForeignKey(
        Post,
        related_name="original_post",
        on_delete=models.CASCADE,
    )
    retalked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    retalk = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="retalks",
    )

    def __str__(self):
        return f"{self.retalked_by} Retalked {self.original_post}"


class PostView(models.Model):
    created_at = models.DateField(auto_now=False, auto_now_add=True)

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="post_view",
    )

    def __str__(self):
        return f"{self.post} Viewed"


class Comment(CommentMixin, TimeStampedModel):
    body = models.TextField()
    media = models.ImageField(
        upload_to=partial(file_upload, "comments_media"),
        null=True,
        blank=True,
    )

    # relations
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    post = models.ForeignKey(
        "network.Post",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    objects = CommentManager()

    def __str__(self):
        return f"{self.user} Comment on {self.post}"


class Contact(models.Model):
    """Intermediary Model >> for not altering User model form django
    and get the time The Realationship was Created
    """

    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )  # Using "db_index" >> improve query performance when ordering QuerySets by this field.

    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_to_set", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class(
    "following",
    models.ManyToManyField(
        "self", through=Contact, related_name="followers", symmetrical=False
    ),
)
