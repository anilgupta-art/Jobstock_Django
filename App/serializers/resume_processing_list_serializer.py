from rest_framework import serializers
from App.models import ResumeProcessing

class ResumeProcessingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeProcessing
        fields = [
            'id', 'user', 'profile', 'job', 'resumesource',
            'resume_path', 'original_filename', 'file_size', 'file_extension',
            'status', 'processing_started_at', 'processing_completed_at',
            'error_message', 'candidate_name', 'extracted_skills',
            'extracted_email', 'extracted_phone', 'years_of_experience',
            'sentiment_score', 'word_count',
        ]
