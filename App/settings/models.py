from django.db import models

class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    client = models.CharField(max_length=100, blank=True, null=True)
    ResponseBody = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
