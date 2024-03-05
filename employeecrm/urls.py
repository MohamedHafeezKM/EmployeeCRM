"""
URL configuration for employeecrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from crm.views import EmployeeCreateView,EmployeeListView,EmployeeDetailView,EmployeeDeleteView,EmployeeUpdateView,RegistrationFormView,SignInView,SignOutView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/add/',EmployeeCreateView.as_view(),name='emp_add'),
    path('employees/all/',EmployeeListView.as_view(),name='all_employees'),
    path('employees/<int:pk>/',EmployeeDetailView.as_view(),name='emp_details'),
    path('employees/<int:pk>/remove',EmployeeDeleteView.as_view(),name='emp_delete'),
    path('employees/<int:pk>/change',EmployeeUpdateView.as_view(),name='emp_change'),
    path('signup/',RegistrationFormView.as_view(),name='signup'),
    path('',SignInView.as_view(),name='signin'),
    path('signout/',SignOutView.as_view(),name='signout'),
    path('api/',include('api.urls'))
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
