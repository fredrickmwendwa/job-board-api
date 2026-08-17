from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Job
from .serializers import JobSerializer
from .permissions import IsCompanyOwner


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def job_list_create_view(request):
    if request.method == 'GET':
        jobs = Job.objects.filter(is_active=True)

        # optional filtering through query params, e.g. ?location=nairobi&job_type=full_time
        location = request.query_params.get('location')
        job_type = request.query_params.get('job_type')

        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'you must be logged in to post a job'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.role != 'company':
            return Response({'error': 'only company accounts can post jobs'}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)

    # from here on, these actions need a logged in owner
    permission = IsCompanyOwner()
    if not request.user.is_authenticated:
        return Response({'error': 'you must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    if not permission.has_object_permission(request, None, job):
        return Response({'error': 'you do not have permission to modify this job'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        job.delete()
        return Response({'message': 'job deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_jobs_view(request):
    # lets a company see every job they've posted, including inactive ones
    if request.user.role != 'company':
        return Response({'error': 'only company accounts have job listings'}, status=status.HTTP_403_FORBIDDEN)

    jobs = Job.objects.filter(posted_by=request.user)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)