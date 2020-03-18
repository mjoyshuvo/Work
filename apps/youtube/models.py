from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class Channel(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, max_length=50)
    channel_uid = models.CharField(null=False, blank=False, max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Video(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, max_length=200)
    channel = models.ForeignKey(Channel, null=False, blank=False, related_name='channels', on_delete=models.CASCADE)
    video_uid = models.CharField(null=False, blank=False, max_length=100, unique=True)
    tags = ArrayField(models.CharField(max_length=300), blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    view_count = models.IntegerField(null=False, blank=False)
    comment_count = models.IntegerField(null=True, blank=True)
    favorite_count = models.IntegerField(null=True, blank=True)
    dislike_count = models.IntegerField(null=True, blank=True)
    # statistics = JSONField()
    performance = models.FloatField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


""" Audit Log Register """
auditlog.register(Channel)
auditlog.register(Video)
