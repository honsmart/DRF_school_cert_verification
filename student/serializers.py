from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    certificate_id = serializers.CharField(max_length=100)
    access_code = serializers.CharField(max_length=10)

    class Meta:
        model = Student
        fields = ['student_name', 'dob', 'department', 'faculty', 'admission_year',
                  'graduation_year', 'certificate_id', 'certificate_image', 'access_code']


class AccessCodeGeneratorSerializer(serializers.Serializer):
    certificate_id = serializers.CharField(max_length=100)
    organization_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=200)

    class Meta:
        model = Student
        fields = ['organization_name', 'email', 'address', 'certificate_id']
