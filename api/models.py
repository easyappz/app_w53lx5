from uuid import uuid4

from django.conf import settings
from django.db import models


class Ad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    source_url = models.URLField(max_length=1000, unique=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=200, default="Без категории")
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.title or self.source_url}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)  # ASC for listing

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user_id} -> {self.ad_id}: {self.text[:30]}"


class SiteSetting(models.Model):
    header_title = models.CharField(max_length=200, default="Авитолог")

    def __str__(self) -> str:  # pragma: no cover
        return f"Settings: {self.header_title}"
