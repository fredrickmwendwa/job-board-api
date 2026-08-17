from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    posted_by_username = serializers.CharField(source='posted_by.username', read_only=True)
    company_name = serializers.CharField(source='posted_by.company_name', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'location', 'job_type',
            'salary_min', 'salary_max', 'is_active',
            'posted_by', 'posted_by_username', 'company_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['posted_by', 'created_at', 'updated_at']