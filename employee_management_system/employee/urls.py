# employee/urls.py
from django.urls import path
from .views import EmployeeIndexView, EmployeeListView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView

urlpatterns = [
    path('', EmployeeIndexView.as_view(), name='index'),
    path('list/', EmployeeListView.as_view(), name='employee_list'),
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('update/<int:employee_id>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('delete/<int:employee_id>/', EmployeeDeleteView.as_view(), name='employee_delete'),
]



