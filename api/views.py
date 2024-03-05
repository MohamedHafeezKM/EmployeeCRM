from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication,permissions
from rest_framework.decorators import action

from crm.models import Employees
from api.serializers import EmployeeSerializer

#APIView
class EmployeeCreateOrListView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        qs=Employees.objects.all()
        #deserializer
        #reference_name=serializerClass(query_set,many=True)   ; many=True is given for more than one item in query_set
        serializer=EmployeeSerializer(qs,many=True)
        
        return Response(data=serializer.data)
    
    def post(self,request,*args,**kwargs):
        #serializer
        print(request.data)
        serializer=EmployeeSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            
            print(serializer.data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

        

class EmployeeDetailOrUpdateOrDelete(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Employees.objects.get(id=id)
        serializer=EmployeeSerializer(qs,many=False)
        print(serializer)
        return Response(data=serializer.data)
    
    def put(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        employee_object=Employees.objects.get(id=id)
        print(request.data)
        serializer=EmployeeSerializer(data=request.data,instance=employee_object)
        if serializer.is_valid():
            serializer.save()
            # print(serializer)
            # print(serializer.data)
            # print(serializer.data)
            return Response(data=serializer.data)
        else:

            return Response(data=serializer.errors)
    
    def delete(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Employees.objects.get(id=id).delete()
        return Response(data={'message':'This employee has been deleted'})
    



#-----------------------viewset--------------------
    
class EmployeeCRUDViewsetView(ViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Employees.objects.all()
   
        print(request.query_params)
        if 'department' in request.query_params:
            value=request.query_params.get('department')
            qs=qs.filter(department__iexact=value)
        deserializer=EmployeeSerializer(qs,many=True)
        return Response(data=deserializer.data)
    
    def create(self,request,*args,**kwargs):
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Employees.objects.get(id=id)
        deserializer=EmployeeSerializer(qs)  #default- many=False
        return Response(data=deserializer.data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        employee_object=Employees.objects.get(id=id)
        serializer=EmployeeSerializer(data=request.data,instance=employee_object)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.erros)
        
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Employees.objects.get(id=id).delete()
        return Response(data={'message':'This employee has been deleted!'})


    #url:localhost:8000/api/v2/employee/all_departments #premade this url by rest_framework
    #method:get   
    @action(methods=['get'],detail=False)
    def all_departments(self,request,*args,**kwargs):
        
        qs=Employees.objects.all().values_list('department',flat=True).distinct()

        return Response(data=qs)