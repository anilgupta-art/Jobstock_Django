

from django.urls import path
from .views import GenerateQuestionsView

urlpatterns = [
	path('generate/<int:call_session_id>/', GenerateQuestionsView.as_view(), name='generate-questions'),
]
