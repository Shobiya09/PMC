from django.db import models

# Create your models here.
class Detail(models.Model):

    name=models.CharField(max_length=100,blank=True,default="")
    phone_no=models.CharField(max_length=10)
    #address=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=12,default="",editable=False)
    user_profileURL=models.URLField(max_length=100,blank=True,default="")
    fcm=models.CharField(max_length=100,blank=True)
    otp=models.CharField(max_length=4,unique=True,default="")
    timestamp=models.CharField(max_length=100,default="")
