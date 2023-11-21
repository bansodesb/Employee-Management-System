from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    identification_document = models.FileField(upload_to='employee_documents/', null=True, blank=True)

    def __str__(self):
        return self.name

