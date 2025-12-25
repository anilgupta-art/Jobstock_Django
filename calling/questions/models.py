

from django.db import models
from calls.models import CallSession

class Question(models.Model):
	call_session = models.ForeignKey(CallSession, on_delete=models.CASCADE, related_name='questions')
	text = models.TextField()
	is_auto_generated = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
