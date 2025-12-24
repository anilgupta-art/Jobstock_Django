

from django.db import models
from calls.models import CallSession

class CallAnalytics(models.Model):
	call_session = models.OneToOneField(CallSession, on_delete=models.CASCADE, related_name='analytics')
	duration_seconds = models.PositiveIntegerField(default=0)
	question_count = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
