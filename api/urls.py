from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views


router=DefaultRouter() #router any varaiable

for u in router.urls:
    print('---------',u,'----------------')

router.register('v2/employees',views.EmployeeCRUDViewsetView,basename='employees')

urlpatterns = [
    path('employees/',views.EmployeeCreateOrListView.as_view()),
    path('employees/<int:pk>/',views.EmployeeDetailOrUpdateOrDelete.as_view())

]+router.urls

#name=' ' is not needed here since we not having any template to pass the name of url