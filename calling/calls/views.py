

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CallSession
from users.models import User

class CreateCallSessionView(APIView):
	def post(self, request):
		# For demo: use first user as caller, or create one if none exists
		caller = User.objects.first()
		if not caller:
			caller = User.objects.create_user(username='demo', password='demo')
		call_type = request.data.get('call_type', 'human_human')
		callee = None
		if call_type == 'human_human':
			callee = User.objects.exclude(id=caller.id).first()
			if not callee:
				callee = User.objects.create_user(username='demo2', password='demo2')
		session = CallSession.objects.create(caller=caller, callee=callee, call_type=call_type)
		return Response({'call_session_id': session.id}, status=status.HTTP_201_CREATED)
