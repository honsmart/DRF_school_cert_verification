from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import random
import string  # Import the string module
from django.core.mail import send_mail
from django.conf import settings
from .models import Student
from .serializers import StudentSerializer, AccessCodeGeneratorSerializer


class VerifyCertificateView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'certificate_id': openapi.Schema(type=openapi.TYPE_STRING, description='Certificate ID'),
            'access_code': openapi.Schema(type=openapi.TYPE_STRING, description='Access code')
        },
        required=['certificate_id', 'access_code']
    ))
    def post(self, request):
        try:
            cert_code = request.data['certificate_id']
            access_code = request.data['access_code']
            print(access_code)
        except KeyError:
            return Response({'error': 'Certificate code and access code are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(
                certificate_id=cert_code, access_code=access_code)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid certificate or access code.'}, status=status.HTTP_404_NOT_FOUND)

        if not student.is_valid:
            return Response({'error': 'Certificate is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(student)
        return Response(serializer.data)


class GenerateAccessCodeView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'certificate_id': openapi.Schema(type=openapi.TYPE_STRING, description='Certificate ID'),
            'organization_name': openapi.Schema(type=openapi.TYPE_STRING, description='Organization Name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address')
        },
        required=['certificate_id', 'organization_name', 'email', 'address']
    ))
    def post(self, request):
        serializer = AccessCodeGeneratorSerializer(data=request.data)
        if serializer.is_valid():
            certificate_id = serializer.validated_data['certificate_id']
            organization_name = serializer.validated_data['organization_name']
            email = serializer.validated_data['email']
            address = serializer.validated_data['address']

            # Generate a random 6-digit access code
            access_code = self.generate_access_code()

            try:
                student = Student.objects.get(certificate_id=certificate_id)
                student.access_code = access_code
                student.organization_name = organization_name
                student.email = email
                student.address = address
                student.save()

                # Send the access code via email using send_mail
                if self.send_access_code_email(email, access_code):
                    return Response({'access_code': access_code}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Failed to send the access code via email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Student.DoesNotExist:
                return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Generate a random 6-digit access code
    def generate_access_code(self):
        # Generate a random string of digits with 6 characters
        access_code = ''.join(random.choices(string.digits, k=6))
        return access_code

    # Send the access code via email using Django's send_mail function
    def send_access_code_email(self, email, access_code):
        try:
            # Create the email message
            subject = "Access Code"
            message = f"Your access code is: {access_code}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            # Use send_mail to send the email
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=False)

            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False
