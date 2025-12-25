

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import VideoRecording
from calls.models import CallSession

class VideoUploadView(APIView):
	parser_classes = (MultiPartParser, FormParser)

	def post(self, request, call_session_id):
		try:
			call_session = CallSession.objects.get(id=call_session_id)
		except CallSession.DoesNotExist:
			return Response({"error": "Call session not found."}, status=status.HTTP_404_NOT_FOUND)

		file_obj = request.FILES.get('file')
		if not file_obj:
			return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

		video_recording, created = VideoRecording.objects.get_or_create(call_session=call_session)
		video_recording.file = file_obj
		video_recording.save()
		return Response({"message": "Video saved.", "file_url": video_recording.file.url}, status=status.HTTP_201_CREATED)
