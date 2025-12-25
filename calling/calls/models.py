

from django.db import models
from users.models import User

class CallSession(models.Model):
	CALL_TYPE_CHOICES = (
		('human_human', 'Human to Human'),
		('human_ai', 'Human to AI'),
	)
	caller = models.ForeignKey(User, related_name='calls_made', on_delete=models.CASCADE)
	callee = models.ForeignKey(User, related_name='calls_received', on_delete=models.CASCADE, null=True, blank=True)
	call_type = models.CharField(max_length=20, choices=CALL_TYPE_CHOICES)
	started_at = models.DateTimeField(auto_now_add=True)
	ended_at = models.DateTimeField(null=True, blank=True)
	is_recorded = models.BooleanField(default=False)
