from django.db import models
from django.db.models import Count, Q, Subquery, Sum

from common.queryset_utils import QuerySetDateHelper
from network.conf import VIDEO


class PostQuerySet(QuerySetDateHelper, models.QuerySet):
    def published(self):
        from network.models import Post
        return self.filter(status=Post.StatusType.PUBLISHED)

    def filter_user_posts(self, user_id):
        return self.filter(Q(user_id=user_id) | Q(mentions__id=user_id))

    def simple_filter_for_user(self, user):
        return (
            self.filter(Q(user__id=user.id))
            .exclude(hidden_from=user)
            .exclude(user__in=user.blocked_users.all())
            .distinct()
        )

    def videos(self):
        return self.filter(type=VIDEO)

    def views_count(self):
        return self.aggregate(views_sum=Sum("views_count")).get("views_sum")

    def annotate_views_in_date_range(self, from_time, to_time):
        return self.annotate(
            post_views_count_in_date_range=Count(
                "post_view",
                filter=Q(
                    post_view__created_at__gt=from_time,
                    post_view__created_at__lt=to_time,
                ),
                distinct=True,
            ),
        )

    def views_count_in_date_range(self, from_time, to_time):
        return (
            self.videos()
            .annotate_views_in_date_range(from_time, to_time)
            .aggregate(
                post_views_count_in_date_range_sum=Sum("post_views_count_in_date_range")
            )
            .get("post_views_count_in_date_range_sum")
        )

    def order_by_top_viewed_date_range(self, from_time, to_time):
        return self.annotate_views_in_date_range(from_time, to_time).order_by(
            "-post_views_count_in_date_range"
        )

    def annotate_anon_reaction_count(self):
        return self.annotate(
            anon_reactions_count=Count(
                "postreaction",
                filter=Q(postreaction__user__isnull=True),
                distinct=True,
            )
        )

    def annotate_users_reaction_count(self):
        return self.annotate(
            users_reactions_count=Count(
                "postreaction",
                filter=Q(postreaction__user__isnull=False),
                distinct=True,
            )
        )


class PostManager(models.Manager.from_queryset(PostQuerySet)):
    pass


class PostReactionQuerySet(QuerySetDateHelper, models.QuerySet):
    def filter_for_user(self, user, *args, **kwargs):
        from network.models import Post

        query = Q(
            Q(
                post_id__in=Subquery(
                    Post.objects.simple_filter_for_user(user).values("id")
                )
            )
            | Q(user_id=user.id)
        )
        return self.filter(query)

    def created_by_user(self):
        return self.filter(user__isnull=False)

    def created_by_anon(self):
        return self.filter(user__isnull=True)


class PostReactionManager(models.Manager.from_queryset(PostReactionQuerySet)):
    pass


class CommentQuerySet(QuerySetDateHelper, models.QuerySet):
    def filter_for_user(self, user, *args, **kwargs):
        from network.models import Post

        query = Q(
            Q(
                post_id__in=Subquery(
                    Post.objects.simple_filter_for_user(user).values("id")
                )
            )
            | Q(user_id=user.id)
        )
        return self.filter(query)


class CommentManager(models.Manager.from_queryset(CommentQuerySet)):
    pass
