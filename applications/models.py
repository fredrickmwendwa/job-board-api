from django.db import models
from django.conf import settings
from jobs.models import Job

from .validators import validate_resume_file




def resume_upload_path(instance, filename):
    # organizes uploads into folders per user, e.g. media/resumes/johndoe/cv.pdf
    return f'resumes/{instance.applicant.username}/{filename}'

resume = models.FileField(upload_to=resume_upload_path, validators=[validate_resume_file])
class Application(models.Model):
    PENDING = 'pending'
    REVIEWED = 'reviewed'
    SHORTLISTED = 'shortlisted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REVIEWED, 'Reviewed'),
        (SHORTLISTED, 'Shortlisted'),
        (REJECTED, 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to=resume_upload_path)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']  # stops someone applying to the same job twice

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"