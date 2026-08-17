import os
from django.core.exceptions import ValidationError


def validate_resume_file(file):
    allowed_extensions = ['.pdf', '.doc', '.docx']
    extension = os.path.splitext(file.name)[1].lower()

    if extension not in allowed_extensions:
        raise ValidationError('resume must be a PDF or Word document (.pdf, .doc, .docx)')

    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'resume file is too large, max size is {max_size_mb}MB')