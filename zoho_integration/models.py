from django.db import models

class ZohoTokenLog(models.Model):
    token_type = models.CharField(max_length=50)
    access_token = models.TextField()
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.token_type} - {self.created_at}"