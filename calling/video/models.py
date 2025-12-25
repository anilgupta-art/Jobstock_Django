

from django.db import models
from calls.models import CallSession

def video_upload_path(instance, filename):
	return f"videos/call_{instance.call_session.id}/{filename}"

class VideoRecording(models.Model):
	call_session = models.OneToOneField(CallSession, on_delete=models.CASCADE, related_name='video_recording')
	file = models.FileField(upload_to=video_upload_path)
	created_at = models.DateTimeField(auto_now_add=True)
