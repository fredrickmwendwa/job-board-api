from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_to_job_view, name='apply-to-job'),
    path('my-applications/', views.my_applications_view, name='my-applications'),
    path('job/<int:job_id>/', views.job_applications_view, name='job-applications'),
    path('<int:pk>/', views.application_detail_view, name='application-detail'),
    path('<int:pk>/status/', views.update_application_status_view, name='application-status'),
]