from django.shortcuts import render,redirect
from crm.forms import EmployeeModelForm,RegistrationForm,LoginForm
from django.views.generic import View
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

# Create your views here.

#create decorator in another file

def signin_required(fn): #fn=get or post
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:  #not works opposite, true become false, false become true
            messages.error(request,'Invalid session,please sign in')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)  #fn=get/post
    return wrapper

@method_decorator(signin_required,name='dispatch') #dispatch decides where to go, to GET or POST
class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeeModelForm()   #instance
        return render(request,'emp_add.html',{'form':form})
 
    def post(self,request,*args,**kwargs):
        form=EmployeeModelForm(request.POST,files=request.FILES) #files=request.FILES, for images and files input;request.POST for text input
        if form.is_valid():
            # Employees.objects.create(**form.cleaned_data) #** is used to unpack dictionery of form.cleaned_data
            form.save() #create & update orm quiry not needed since modelForm have benfit by form.save() function to save to database
            messages.success(request,'The employee add been added successfully')
           #message.type(request,'the message you want to print on html')
            return redirect('all_employees')
        
        else:
            messages.error(request,'Failed to add the employee,pls try again')
            return render(request,'emp_add.html',{'form':form})
        
@method_decorator(signin_required,name='dispatch')
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        # if request.user.is_authenticated:
        qs=Employees.objects.all()
        departments=Employees.objects.all().values_list('department',flat=True).distinct()
        # print(departments) values_list is given to take an enitire coloum of department,flat=True is to remove tuples formed,.distinct() is given to remove repeating department


        #request.GET is a dictionery
        #localhost/employee/all?department=HR -->searching meathod by url; '?' stands for optional query
        if 'department' in request.GET:
            # print(request.GET)
            dept=request.GET.get('department')
            qs=qs.filter(department__iexact=dept) #__iexact will ignore all uppercase and lowercases ,ormquiery
            # print(qs)
        return render(request,'all_empolyees.html',{'data':qs,'departments':departments})
        # else:
        #     messages.error(request,'Invalid Session')
        #     return redirect('signin')

        
    
    def post(self,request,*args,**kwargs):
        name=request.POST.get('box') #box is the id of input box from search
        # qs=Employees.objects.filter(name=name) #accurate
        qs=Employees.objects.filter(name__icontains=name)  #apporixmate; __icontain helps to get the query data that macthes the keyword that we gave
        lst=[i for i in qs]
        print(lst)
        if lst==[]:
            messages.error(request,'Not Found')
            return render(request,'all_empolyees.html',{'data':qs})
        else:
            messages.success(request,'Found details')
            return render(request,'all_empolyees.html',{'data':qs})
       
        
    
    

@method_decorator(signin_required,name='dispatch')
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        print(kwargs)
        id=kwargs.get('pk') #kwargs={'pk':1} pk meaning primary key
        qs=Employees.objects.get(id=id)
        return render(request,'emp_details.html',{'data':qs})
        

@method_decorator(signin_required,name='dispatch')
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Employees.objects.get(id=id).delete()
        messages.success(request,'Employee has been deleted sucessfullly')
        return redirect('all_employees')

@method_decorator(signin_required,name='dispatch')
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(instance=obj) #'instance=' means intilising,alreay fill the form with matching data from database,instance only works with modelform, can be used for other forms
        return render(request,'emp_edit.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(request.POST,files=request.FILES,instance=obj) #autoupdate, the request.POST along with 'instance=' will update when save() is given
        if form.is_valid():
            form.save() #autoupdate using instance and request.POST datas
            messages.success(request,'This employee details had been updated')
            return redirect('emp_details',pk=id)  #redirect(x,y) redirect have two paramater,x=url name, y=<int:pk> or id
        
        else:
            messages.error(request,'Failed to update employee')
            return render(request,'emp_edit.html',{'form':form})
            

class RegistrationFormView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,'signup.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save() form.save saves the password without encryption in database
            User.objects.create_user(**form.cleaned_data) #create_user helps to create an user with encrypted password in auth user db
            messages.success(request,'The admin added')
            return redirect('signin')
        else:
            messages.error(request,'Failed to create account')
            return render(request,'signup.html',{'form':form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'signin.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            pass_word=form.cleaned_data.get('password')
            # print(user_name,pass_word)
            user_object=authenticate(request,username=user_name,password=pass_word) #default djagno function authenticate(request,username,password): returns User object if valid else: retunrs None Value
            if user_object:
                # print('valid')
                # print(user_object)
                login(request,user_object) #defaultdjango, def login(request,user) user session starting
                # print(request.user) #request.user will give you which user on right now;request.user=user_object
                return redirect('all_employees')
                 #This way a user doesn't have to reauthenticate on every request.
        messages.error(request,'Invalid Credential')   #else not needed here #these last two steps don't work if redirect works
        return render(request,'signin.html',{'form':form})


            # else:
            #     print('invalid')
            #     messages.error(request,'Invalid Credential')

            #     return render(request,'signin.html',{'form':form})
        
        # else:
   
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)  #def logout(request) default function from django.contrib.auth
        messages.success(request,'Succesfully logged out')
        return redirect('signin')
