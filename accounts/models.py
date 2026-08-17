from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # a user is either someone looking for a job, or a company posting jobs
    JOB_SEEKER = 'job_seeker'
    COMPANY = 'company'

    ROLE_CHOICES = [
        (JOB_SEEKER, 'Job Seeker'),
        (COMPANY, 'Company'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=JOB_SEEKER)
    phone_number = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=150, blank=True)  # only used if role is company

    def __str__(self):
        return self.username