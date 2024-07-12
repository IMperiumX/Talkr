from functools import partial

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from common.utils import file_upload
from network.conf import LIKE_REACTION
from network.managers import CommentManager, PostManager, PostReactionManager
from network.model_mixins import CommentMixin, PostMixin, PostReactionMixin


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(default="default.png", upload_to="users/%Y/%m/%d/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile for user {self.user.username}"

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.id)])


class PublishedQuerySet(models.QuerySet):

    use_for_related_fields = True

    def published(self):
        return self.filter(status="published")


class Post(PostMixin, models.Model):
    class StatusType(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    # fields
    body = models.TextField(max_length=280, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=StatusType.choices,
        default=StatusType.DRAFT,
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_user", blank=True
    )
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    # relations
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="twitter_posts",
        null=True,
    )

    objects = PostManager()

    def __str__(self):
        return self.body[:50] + "..."

    class Meta:
        ordering = ("-publish",)

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])


class PostReaction(PostReactionMixin, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    # reactions
    LIKE_REACTION = LIKE_REACTION
    reaction = models.CharField(
        max_length=20,
        choices=((LIKE_REACTION, LIKE_REACTION),),
    )
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    # managers
    objects = PostReactionManager()

    class Meta:
        unique_together = (("user", "post"),)


class PostView(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_view")
    created_at = models.DateField(auto_now=False, auto_now_add=True)


class Comment(CommentMixin, models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment"
    )
    picture = models.ImageField(
        upload_to=partial(file_upload, "comment_pictures"), null=True, blank=True
    )
    text = models.TextField()
    created_at = models.DateField(auto_now=False, auto_now_add=True)

    # managers
    objects = CommentManager()


class Contact(models.Model):
    """Intermediary Model >> for not altering User model form django
    and get the time The Realationship was Created
    """

    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True
    )  # Using "db_index" >> improve query performance when ordering QuerySets by this field.

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
