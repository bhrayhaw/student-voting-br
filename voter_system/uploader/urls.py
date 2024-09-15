from django.urls import path
from .views import upload_file, list_students

urlpatterns = [
    path('upload/', upload_file, name='upload'),
    path('students/', list_students, name='students'),
]
