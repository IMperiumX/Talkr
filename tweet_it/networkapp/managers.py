from django.db import models


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published")


class PostManager(models.Manager.from_queryset(PostQuerySet)):
    pass
