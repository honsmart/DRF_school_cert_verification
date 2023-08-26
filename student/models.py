from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    certificate_id = models.CharField(max_length=10, unique=True)
    student_name = models.CharField(max_length=200)
    dob = models.DateField()
    department = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    admission_year = models.PositiveIntegerField()
    graduation_year = models.PositiveIntegerField()
    access_code = models.CharField(max_length=10, unique=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"Certificate ID: {self.certificate_id}, Student ID: {self.student_id}, Student Name: {self.student_name}"
