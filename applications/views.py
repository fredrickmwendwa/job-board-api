from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from jobs.models import Job
from .models import Application
from .serializers import ApplicationSerializer, ApplicationStatusUpdateSerializer
from .permissions import IsApplicantOrJobOwner


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def apply_to_job_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.user.role != 'job_seeker':
        return Response({'error': 'only job seekers can apply to jobs'}, status=status.HTTP_403_FORBIDDEN)

    if not job.is_active:
        return Response({'error': 'this job is no longer accepting applications'}, status=status.HTTP_400_BAD_REQUEST)

    if Application.objects.filter(job=job, applicant=request.user).exists():
        return Response({'error': 'you have already applied to this job'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(applicant=request.user, job=job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications_view(request):
    # a job seeker tracking everything they've applied to
    if request.user.role != 'job_seeker':
        return Response({'error': 'only job seekers have applications to track'}, status=status.HTTP_403_FORBIDDEN)

    applications = Application.objects.filter(applicant=request.user)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_applications_view(request, job_id):
    # a company viewing everyone who applied to one specific job listing
    job = get_object_or_404(Job, pk=job_id)

    if request.user != job.posted_by:
        return Response({'error': 'you can only view applications for your own job postings'}, status=status.HTTP_403_FORBIDDEN)

    applications = Application.objects.filter(job=job)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def application_detail_view(request, pk):
    application = get_object_or_404(Application, pk=pk)

    permission = IsApplicantOrJobOwner()
    if not permission.has_object_permission(request, None, application):
        return Response({'error': 'you do not have permission to view this application'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    if request.method == 'DELETE':
        # only the applicant can withdraw their own application, not the company
        if request.user != application.applicant:
            return Response({'error': 'only the applicant can withdraw an application'}, status=status.HTTP_403_FORBIDDEN)
        application.delete()
        return Response({'message': 'application withdrawn'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_application_status_view(request, pk):
    application = get_object_or_404(Application, pk=pk)

    # only the company that owns the job can change the status
    if request.user != application.job.posted_by:
        return Response({'error': 'only the company that posted this job can update application status'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ApplicationStatusUpdateSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(ApplicationSerializer(application).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)