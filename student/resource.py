from import_export import resources 
from .models import Student

class ReportResource(resources.ModelResource):
     class Meta:
         model = Student