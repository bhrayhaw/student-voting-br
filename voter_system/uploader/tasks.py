import pandas as pd
import os
from celery import shared_task
from .models import Student
from django.core.mail import send_mail

@shared_task
def process_file(file_path, admin_email):
    try:
        # Read the file with pandas based on file extension
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            return f'Unsupported file type: {file_path}'

        # Process each row and save it in the database
        for _, row in data.iterrows():
            Student.objects.create(
                student_id=row['student_id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                department=row['department']
            )

        # Send an email to notify the admin after successful processing
        send_mail(
            subject='Student File Processing Completed',
            message=f'The file {file_path} has been processed successfully.',
            from_email= os.getenv('ADMIN_EMAIL'),  
            recipient_list=[admin_email],  
        )
        
        return 'File processed successfully and email sent'
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return f'Error: {str(e)}'
