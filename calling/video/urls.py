

from django.urls import path
from .views import VideoUploadView

urlpatterns = [
	path('upload/<int:call_session_id>/', VideoUploadView.as_view(), name='video-upload'),
]
