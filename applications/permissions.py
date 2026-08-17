from rest_framework import permissions


class IsApplicantOrJobOwner(permissions.BasePermission):
    """
    the applicant who submitted it can view it
    the company that owns the job it was submitted to can also view it
    nobody else can
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.applicant:
            return True
        if request.user == obj.job.posted_by:
            return True
        return False