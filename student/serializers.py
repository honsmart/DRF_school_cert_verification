from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    certificate_id = serializers.CharField(max_length=100)
    access_code = serializers.CharField(max_length=10)

    class Meta:
        model = Student
        fields = ['student_name','dob','department','faculty','admission_year','graduation_year','certificate_id', 'access_code']
