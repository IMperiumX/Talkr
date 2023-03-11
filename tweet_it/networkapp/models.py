from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .conf import STATUS_CHOICES
from .managers import PostManager

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(default="default.png", upload_to="users/%Y/%m/%d/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile for user {self.user.username}"

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.id)])


class Post(models.Model):
    body = models.TextField(max_length=280, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0],
    )
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="twitter_posts",
        null=True,
    )
    users_like = models.ManyToManyField(
        User,
        related_name="liked_user",
        blank=True,
    )

    objects = PostManager()

    def __str__(self):
        return self.body[:50] + "..."

    class Meta:
        ordering = ("-publish",)

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])


class Contact(models.Model):
    """Intermediary Model >> for not altering User model form django
    and get the time The Realationship was Created
    """

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    user_from = models.ForeignKey(
        User,
        related_name="rel_from_set",
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        User,
        related_name="rel_to_set",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"
