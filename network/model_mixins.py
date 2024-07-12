import os

from django.core.files import File
from django_lifecycle import LifecycleModelMixin, hook
from django_lifecycle.hooks import AFTER_CREATE, BEFORE_DELETE

from common.utils import get_thumbnail_from_video, get_unique_string
from network.constants import *


class OwnerPermission:
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return self.user_id == request.user.id

    def has_object_update_permission(self, request):
        return self.user_id == request.user.id


class PostVideoRenderMixin:
    def save_thumbnail(self):
        post = self
        if not post.video:
            return

        # check if has readable video
        post_video = post.video.read()
        if not post_video:
            return

        # save video
        video_path = f"/tmp/{get_unique_string()}.mp4"

        with open(video_path, "wb") as vf:
            vf.write(post_video)

        # generate thumbnail
        image_path = get_thumbnail_from_video(video_path)

        # # save thumbnail
        with open(image_path, "rb") as f:
            post.video_thumbnail.save("new.jpg", File(f))

        # # remove temp files
        os.remove(video_path)
        os.remove(image_path)


class PostPermissionMixin(OwnerPermission):
    def has_object_toggle_like_permission(self, request):
        return True

    def has_object_hide_permission(self, request):
        return bool(request.user.id)

    def has_object_increment_views_permission(self, request):
        return True

    def has_object_destroy_permission(self, request):
        user = request.user
        if not user.is_authenticated:
            return False
        return self.user_id == user.id


class PostMixin(
    PostVideoRenderMixin,
    PostPermissionMixin,
):
    def increment_views_count(self):
        if not self.views_count:
            self.views_count = 0
        self.views_count += 1
        self.save()
        self.post_view.create(post=self)

    def toggle_like(self, user):
        """toggle like for a post

        Returns:
            created: if the like was added or removed
            error: if the user is not allowed to like the post
        """
        if not user.is_authenticated:
            self.reactions.create(
                user=None,
                reaction=LIKE,
            )
            return True, None

        if self.is_liked_by(user):
            self.reactions.filter(user_id=user.id).delete()
            return False, None

        self.reactions.create(
            user=user,
            reaction=LIKE,
        )
        return True, None

    @property
    def life_reaction_count(self):
        return self.reactions.all().count()

    @property
    def is_video(self):
        return self.type == VIDEO


""" Post Reaction """


class PostReactionMixin(LifecycleModelMixin, OwnerPermission):
    @staticmethod
    def has_write_permission(request):
        return False

    def has_object_write_permission(self, request):
        return False

    def has_object_update_permission(self, request):
        return False

    @hook(AFTER_CREATE)
    def after_reaction_create(self):
        self.post.reactions_count = self.post.life_reaction_count
        self.post.save()

    @hook(BEFORE_DELETE)
    def before_reaction_delete(self):
        self.post.reactions_count = self.post.life_reaction_count - 1
        self.post.save()


class CommentMixin(LifecycleModelMixin, OwnerPermission):
    @hook(AFTER_CREATE)
    def after_comment_create(self):
        self.post.comments_count = self.post.comments_count + 1
        self.post.save()

    @hook(BEFORE_DELETE)
    def before_comment_delete(self):
        self.post.comments_count = self.post.comments_count - 1
        self.post.save()
