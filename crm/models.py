from django.db import models

# Create your models here.

class Employees(models.Model):
    name=models.CharField(max_length=100)
    department=models.CharField(max_length=100) #for Charfield, max_length is needed
    salary=models.PositiveIntegerField()
    email=models.EmailField(unique=True)  #unique=True means same email cannot be used for other ids
    age=models.PositiveIntegerField()
    contact=models.CharField(null=True,max_length=10)
    image=models.ImageField(upload_to='images',null=True,blank=True) #null for database,blank=True for form,i.e. form will accept without picture
    date_of_birth=models.DateField(null=True,blank=True)

    def __str__(self):    #object string represntation
        return self.name   


    # convert all these attributes to Queryfile
    # for that code:python manage.py makemigrations
    # to execute queryfile to database
    #for that code:python manage.py migrate