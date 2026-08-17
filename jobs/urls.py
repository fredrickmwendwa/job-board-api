from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list_create_view, name='job-list-create'),
    path('my-jobs/', views.my_jobs_view, name='my-jobs'),
    path('<int:pk>/', views.job_detail_view, name='job-detail'),
]