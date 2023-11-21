from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest

# Create your views here.

class EmployeeIndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class EmployeeListView(View):
    template_name = 'employee_list.html'

    def get(self, request):
        search_query = request.GET.get('q', '')

        if search_query:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM employee_employee WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(position) LIKE LOWER(%s) OR LOWER(department) LIKE LOWER(%s)",
                               [f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
                employees = cursor.fetchall()
        else:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM employee_employee")
                employees = cursor.fetchall()

        return render(request, self.template_name, {'employees': employees, 'search_query': search_query})


class EmployeeCreateView(View):
    template_name = 'add_new_employee.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        position = request.POST.get('position')
        department = request.POST.get('department')
        salary = request.POST.get('salary')
        identification_document = request.FILES.get('identification_document')

        if identification_document and not identification_document.name.endswith('.pdf'):
            return HttpResponseBadRequest("Only PDF files are allowed.")

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO employee_employee (name, position, department, salary, identification_document) VALUES (%s, %s, %s, %s, %s)",
                           [name, position, department, salary, identification_document.name])

        fs = FileSystemStorage()
        fs.save(f'employee_documents/{identification_document.name}', identification_document)

        return redirect('employee_list')


class EmployeeUpdateView(View):
    template_name = 'add_new_employee.html'

    def get(self, request, employee_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee_employee WHERE id = %s", [employee_id])
            employee = cursor.fetchone()

        return render(request, self.template_name, {'employee': employee})

    def post(self, request, employee_id):
        name = request.POST.get('name')
        position = request.POST.get('position')
        department = request.POST.get('department')
        salary = request.POST.get('salary')
        identification_document = request.FILES.get('identification_document')

        if identification_document and not identification_document.name.endswith('.pdf'):
            return HttpResponseBadRequest("Only PDF files are allowed.")

        with connection.cursor() as cursor:
            cursor.execute("UPDATE employee_employee SET name=%s, position=%s, department=%s, salary=%s, identification_document=%s WHERE id=%s",
                           [name, position, department, salary, identification_document.name, employee_id])

        if identification_document:
            fs = FileSystemStorage()
            fs.save(f'employee_documents/{identification_document.name}', identification_document)

        return redirect('employee_list')


class EmployeeDeleteView(View):
    template_name = 'employee_confirm_delete.html'

    def get(self, request, employee_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee_employee WHERE id = %s", [employee_id])
            employee = cursor.fetchone()

        return render(request, self.template_name, {'employee': employee})

    def post(self, request, employee_id):
        confirm_delete = request.POST.get('confirm_delete')

        if confirm_delete == 'yes':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM employee_employee WHERE id=%s", [employee_id])

            return redirect('employee_list')
        else:
            return HttpResponseBadRequest("Deletion canceled.")
