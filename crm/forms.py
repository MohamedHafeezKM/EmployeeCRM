from django.forms import Form,CharField,IntegerField,EmailField,TextInput,EmailInput,NumberInput,ModelForm,Textarea,PasswordInput,DateInput
from crm.models import Employees
from django.contrib.auth.models import User

# class EmployeeForm(Form):
#     name=CharField(widget=TextInput(attrs={"class":"form-control"}))
#     department=CharField(widget=TextInput(attrs={"class":"form-control"}))
#     salary=IntegerField(widget=TextInput(attrs={"class":"form-control"}))
#     email=EmailField(widget=EmailInput(attrs={"class":"form-control"}))
#     age=IntegerField(widget=NumberInput(attrs={"class":"form-control"}))
#     contact=CharField(widget=TextInput(attrs={"class":"form-control"}))



class EmployeeModelForm(ModelForm): #all fields from model get automatically populated here instead of creating every new form field

    class Meta:
        model=Employees   #our model, database name
        fields='__all__'    #all fields ['name','department...]


        #stylying, input type      and        bootstrap
        widgets={
            'name':TextInput(attrs={'class':'form-control'}),
            'department':TextInput(attrs={'class':'form-control'}),
            'salary':NumberInput(attrs={'class':'form-control'}),
            'email':EmailInput(attrs={'class':'form-control'}),
            'age':NumberInput(attrs={'class':'form-control'}),
            'contact':Textarea(attrs={'class':'form-control','rows':5}),
                                                            # 5rows text box area is given
            'date_of_birth':DateInput(attrs={'class':'form-control','type':'date'})
        }


class RegistrationForm(ModelForm):

    class Meta:
        model=User  #from auth.models default model class User, User is inherited from AbsratctBaseUser and AbstractUser
        fields=['username','email','password'] #only these field from default needed on our form
        widgets={
            'username':TextInput(attrs={'class':'form-control'}),
            'email':EmailInput(attrs={'class':'form-control'}),
            'password':PasswordInput(attrs={'class':'form-control'})
        }
        #class AbsratctBaseUser(Model):
        # password=charfield()
        # username=charfiled()

        # class AbstractUser(AbstractBaseUser):
        # first_name=charfiled()
        # last_name=charfield()
        # email=emailfield()

        # class User(AbstractUser):
        # inhertied all AbstarctBaseUser and AbstarctUser 

class LoginForm(Form): #we dont' use ModelForm here since we are not creating nor updating anything to database
    username=CharField(widget=TextInput(attrs={'class':'form-control'}))
    password=CharField(widget=PasswordInput(attrs={'class':'form-control'}))