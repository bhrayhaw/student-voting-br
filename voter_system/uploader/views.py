import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from django.core.files.storage import default_storage

@api_view(['POST'])
def upload_file(request):
    try:
        file = request.FILES.get('file', None)

        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = default_storage.save(f'uploads/{file.name}', file)
        full_file_path = default_storage.path(file_path)  # Get the full path
        
        # Read the file with pandas
        if file.name.endswith('.csv'):
            data = pd.read_csv(full_file_path)
        elif file.name.endswith('.xlsx'):
            data = pd.read_excel(full_file_path)
        else:
            return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process each row and save it in the database
        for _, row in data.iterrows():
            Student.objects.create(
                student_id=row['student_id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                department=row['department']
            )

        return Response({'message': 'File uploaded and processed successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
