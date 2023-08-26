from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Student
from .serializers import StudentSerializer

class VerifyCertificateView(APIView):
    @swagger_auto_schema( request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'certificate_id': openapi.Schema(type=openapi.TYPE_STRING, description='Certificate ID'),
                'access_code': openapi.Schema(type=openapi.TYPE_STRING, description='Access code')
            },
            required=[ 'certificate_id', 'access_code']
        ))
    def post(self, request):
        try:
            cert_code = request.data['certificate_id']
            access_code = request.data['access_code']
            print(access_code)
        except KeyError:
            return Response({'error': 'Certificate code and access code are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(certificate_id=cert_code, access_code=access_code)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid certificate or access code.'}, status=status.HTTP_404_NOT_FOUND)

        if not student.is_valid:
            return Response({'error': 'Certificate is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(student)
        return Response(serializer.data)
