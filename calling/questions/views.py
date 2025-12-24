

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from calls.models import CallSession
import random

# Example static question pool (replace with ML/OpenAI logic as needed)
STATIC_QUESTIONS = [
	"How did you feel about the call?",
	"Was the video quality satisfactory?",
	"Would you recommend this service?",
	"Did you face any technical issues?",
	"How can we improve your experience?"
]

class GenerateQuestionsView(APIView):
	def post(self, request, call_session_id):
		try:
			call_session = CallSession.objects.get(id=call_session_id)
		except CallSession.DoesNotExist:
			return Response({"error": "Call session not found."}, status=status.HTTP_404_NOT_FOUND)

		# For demo: randomly select 3 questions
		selected = random.sample(STATIC_QUESTIONS, 3)
		questions = []
		for q in selected:
			question = Question.objects.create(
				call_session=call_session,
				text=q,
				is_auto_generated=True
			)
			questions.append(question.text)
		return Response({"questions": questions}, status=status.HTTP_201_CREATED)
