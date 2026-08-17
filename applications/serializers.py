from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_username = serializers.CharField(source='applicant.username', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'applicant', 'applicant_username',
            'resume', 'cover_letter', 'status', 'applied_at', 'updated_at',
        ]
        read_only_fields = ['applicant', 'status', 'applied_at', 'updated_at']


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']