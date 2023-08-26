from django.contrib import admin
from student.models import Student
from import_export.admin import ImportExportModelAdmin
from .resource import ReportResource  

class ReportAdmin(ImportExportModelAdmin):
     resource_class = ReportResource      




admin.site.register(Student, ReportAdmin)
