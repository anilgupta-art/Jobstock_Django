

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	USER_TYPE_CHOICES = (
		('human', 'Human'),
		('system', 'System'),
		('ai', 'AI'),
	)
	user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='human')
