from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.models import TimeStampedModel


class Action(models.Model):
    user = models.ForeignKey(
        "auth.User",
        related_name="actions",
        db_index=True,
        on_delete=models.CASCADE,
    )
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey("target_ct", "target_id")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user} {self.verb} {self.target}"


class Block(TimeStampedModel):
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="blocker",
        on_delete=models.CASCADE,
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="blocked",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
