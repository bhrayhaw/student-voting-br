import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from django.core.files.storage import default_storage
from .tasks import process_file


@api_view(['POST'])
def upload_file(request):
    try:
        file = request.FILES.get('file', None)
        admin_email = request.data.get('admin_email', os.getenv('ADMIN_EMAIL'))

        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the file temporarily
        file_path = default_storage.save(f'uploads/{file.name}', file)
        full_file_path = default_storage.path(file_path) 
        
        # Dispatch Celery task to process the file asynchronously and send an email
        process_file.delay(full_file_path, admin_email) 

        return Response({'message': 'File uploaded and processing has started'}, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
