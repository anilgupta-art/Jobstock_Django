

from django.urls import path
from .views import CreateCallSessionView

urlpatterns = [
	path('create/', CreateCallSessionView.as_view(), name='create-call-session'),
]
