from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Student
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import pandas as pd


class StudentUploadTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.upload_url = reverse('upload')  # Make sure the URL name matches the one you used in urls.py
        self.students_url = reverse('students')  # The endpoint to list students

    def test_upload_csv_file(self):
        """Test uploading a valid CSV file."""
        data = """student_id,first_name,last_name,email,department
        1,John,Doe,johndoe@example.com,Computer Science
        2,Jane,Doe,janedoe@example.com,Physics"""
        
        # Use SimpleUploadedFile to simulate file upload
        csv_file = SimpleUploadedFile("students.csv", data.encode('utf-8'), content_type="text/csv")

        # Post the CSV file as multipart/form-data
        response = self.client.post(self.upload_url, {'file': csv_file}, format='multipart')

        print(response.content)  # Debug the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.count(), 2)  # Ensure students were created

    def test_upload_excel_file(self):
        """Test uploading a valid Excel file."""
        df = pd.DataFrame({
            'student_id': [1, 2],
            'first_name': ['John', 'Jane'],
            'last_name': ['Doe', 'Doe'],
            'email': ['johndoe@example.com', 'janedoe@example.com'],
            'department': ['Computer Science', 'Physics'],
        })

        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False, engine='openpyxl')
        excel_file.seek(0)  # Reset the file pointer to the start

        # Create a Django SimpleUploadedFile for the Excel file
        excel_file_django = SimpleUploadedFile(
            "students.xlsx", excel_file.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Post the Excel file as multipart/form-data
        response = self.client.post(self.upload_url, {'file': excel_file_django}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.count(), 2)  # Ensure two students were created

    def test_student_list(self):
        """Test retrieving a list of students."""
        # Create sample students
        Student.objects.create(student_id='1', first_name='John', last_name='Doe', email='johndoe@example.com', department='CS')
        Student.objects.create(student_id='2', first_name='Jane', last_name='Doe', email='janedoe@example.com', department='Physics')

        response = self.client.get(self.students_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure the correct number of students is returned

    def test_upload_invalid_file(self):
        """Test uploading an invalid file format."""
        invalid_file = SimpleUploadedFile("invalid.txt", b"Invalid content", content_type="text/plain")
        response = self.client.post(self.upload_url, {'file': invalid_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
