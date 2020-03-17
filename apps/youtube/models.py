from django.db import models
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


# class Channel(models.Model):
#     history = AuditlogHistoryField()
#     name = models.CharField(null=False, blank=False, max_length=50)
#     channel_uid = models.CharField(null=False, blank=False, max_length=80, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return "{}".format(self.name)
#
#
# class Video(models.Model):
#     history = AuditlogHistoryField()
#     name = models.CharField(null=False, blank=False, max_length=200)
#     video_uid = models.CharField(null=False, blank=False, max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name

class Test(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, max_length=10)
    data = models.CharField(null=True, blank=True, max_length=10)


""" Audit Log Register """
# auditlog.register(Banks)
# auditlog.register(Company)
auditlog.register(Test)
