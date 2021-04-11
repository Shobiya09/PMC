from rest_framework import serializers
from User.models import Detail
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate,login
from rest_framework import filters
import random
import smtplib
from datetime import datetime
import re

def URLValid(url):
    if url=="":
        return url
    # Regex to check valid URL
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    # Compile the ReGex
    p = re.compile(regex)
    if re.search(p, url)==False:
        raise serializers.ValidationError(["URL is not valid"])
    return url

def PswValid(psw):
    l=list(psw)
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    res = any(chr.isdigit() for chr in psw)
    upper = any(ele.isupper() for ele in psw)
    lower = any(ele.islower() for ele in psw)
    if len(l)<4 or len(l)>12:
        raise serializers.ValidationError({
                                        "status_type": "false",
                                        "entity": [
                                            {
                                                "password":  psw
                                            }
                                        ],
                                        "entity_type": "JsonArrays",
                                        "entity_status": "1",
                                        "entity_msg": "New user details update is failed.password should be between 4 to 12 characters",
                                        "status": "202"
                                    })
    elif(regex.search(psw) == None):
        raise serializers.ValidationError({
                                        "status_type": "false",
                                        "entity": [
                                            {
                                                "password":  psw
                                            }
                                        ],
                                        "entity_type": "JsonArrays",
                                        "entity_status": "1",
                                        "entity_msg": "New user details update is failed.password should contain atleast 1 special charater",
                                        "status": "202"
                                    })
    elif (res==False):
        raise serializers.ValidationError({
                                                "status_type": "false",
                                                "entity": [
                                                    {
                                                        "password":  psw
                                                    }
                                                ],
                                                "entity_type": "JsonArrays",
                                                "entity_status": "1",
                                                "entity_msg": "New user details update is failed.password should contain atleast 1 number",
                                                "status": "202"
                                            })
    elif (upper==False or lower== False):
        raise serializers.ValidationError({
                                                "status_type": "false",
                                                "entity": [
                                                    {
                                                        "password":  psw
                                                    }
                                                ],
                                                "entity_type": "JsonArrays",
                                                "entity_status": "1",
                                                "entity_msg": "New user details update is failed.password should contain atleast 1 uppercase or lowercase ",
                                                "status": "202"
                                            })
    return psw



def NameValid(name):
    if name == "":
        raise serializers.ValidationError(["Give user name"])
    return name

def PhoneValid(phn):
    l=list(phn)
    if len(l)<10 or len(l)>10 :
        raise serializers.ValidationError({
                                        "status_type": "false",
                                        "entity": [
                                            {
                                                "phone_no":  phn
                                            }
                                        ],
                                        "entity_type": "JsonArrays",
                                        "entity_status": "1",
                                        "entity_msg": "New user details update is failed.",
                                        "status": "202"
                                    })
    return phn


class UserAuthenticaton(serializers.ModelSerializer):
    class Meta:
        model=Detail
        fields=['name','phone_no','email','user_profileURL','fcm','password']
        extra_kwargs = {
        'email': {'validators': [EmailValidator,]},
    }


    #email=serializers.EmailField()
    name=serializers.CharField(validators = [NameValid],allow_blank=False)
    phone_no=serializers.CharField(validators=[PhoneValid],allow_blank=False)
    user_profileURL=serializers.URLField(validators=[URLValid],allow_blank=True)
    fcm=serializers.CharField(max_length=100,allow_blank=True)
    password=serializers.CharField(validators=[PswValid])


class LoginSerializer(serializers.Serializer):
    class Meta:
        model=Detail
        fields=['email','password','fcm']

    email=serializers.EmailField()
    password=serializers.CharField()
    #fcm=serializers.CharField(max_length=100,allow_blank=True)

    def validate(self,data):
        email1=data.get("email", "")
        password1=data.get("password", "")
        email2=Detail.objects.filter(email=email1)
        password2=Detail.objects.filter(password=password1)
        #user=Detail.objects.get(email=email1)
        if email1 and password1:
            if email2:
                if password2:
                    return 1
                else:
                    raise serializers.ValidationError({
                                                        "status_type": "false",
                                                        "entity":
                                                            {
                                                                "mail_id": email1,
                                                                "password":password1
                                                            }
                                                        ,
                                                        "entity_type": "JsonArrays",
                                                        "entity_status": "1",
                                                       "entity_msg": "User password is invalid.",
                                                        "status": "202"
                                                    })
            else:
                raise serializers.ValidationError({
                                                    "status_type": "false",
                                                    "entity":
                                                        {
                                                            "mail_id": email1,
                                                            "password":password1
                                                        }
                                                    ,
                                                    "entity_type": "JsonArrays",
                                                    "entity_status": "1",
                                                    "entity_msg": "User Mail ID and Password is invalid.",
                                                    "status": "202"
                                                })

        else:
            raise serializers.ValidationError(["must provide username and password both"])


class ChangepswSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    new_password=serializers.CharField(validators=[PswValid])
    class Meta:
        model=Detail
        fields=['email','password']
    def validate(self,data):
        email1=data.get("email", "")
        password1=data.get("password", "")
        new_password1=data.get("new_password","")
        email2=Detail.objects.filter(email=email1)
        password2=Detail.objects.filter(password=password1)
        if email2:
            if password2:
                Detail.objects.filter(email=email1).update(password=new_password1)
                return data
            else:
                raise serializers.ValidationError({
                                                    "status_type": "false",
                                                    "entity": [
                                                       {
                                                	"mail_id": email1,
                                                "old_password":password1,
                                                "new_password":new_password1,
                                                }
                                                    ],
                                                    "entity_type": "JsonArrays",
                                                    "entity_status": "1",
                                                    "entity_msg": "User old password to change new password is invalid.",
                                                    "status": "202"
                                                })
        else:
            raise serializers.ValidationError({
                                                    "status_type": "false",
                                                    "entity": [
                                                       {
                                                	"mail_id": email1,
                                                "old_password":password1,
                                                "new_password":new_password1,
                                                }
                                                    ],
                                                    "entity_type": "JsonArrays",
                                                    "entity_status": "1",
                                                    "entity_msg": "give a valid email id",
                                                    "status": "202"
                                                })

class otpSerializer(serializers.Serializer):
    email=serializers.EmailField()
    class Meta:
        model=Detail
        fields=['email']
    def validate(self,data):
        email1=data.get("email", "")
        email2=Detail.objects.filter(email=email1)
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        if email2:
            email3=Detail.objects.get(email=email1)
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login('pcm.otp.generator@gmail.com','otpgenerator')
            otp1=''.join([str(random.randint(0,9)) for i in range(4)])
            Detail.objects.filter(email=email1).update(otp=otp1)
            now = datetime.now()
            timestamp1 = datetime.timestamp(now)
            Detail.objects.filter(email=email1).update(timestamp=timestamp1)
            msg="hi,your otp is"+otp1
            server.sendmail('pcm.otp.generator@gmail.com',email3.email,msg)
            server.quit()
            return data
        else:
            raise serializers.ValidationError({
                                                "status_type": "false",
                                                "entity": [
                                                    {
                                                        "mail_id": email1
                                                    }
                                                ],
                                                "entity_type": "JsonArrays",
                                                "entity_status": "1",
                                                "entity_msg": "User OTP generator is failed",
                                                "status": "202"
                                            })

class otpvalidSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField()
    new_password=serializers.CharField()
    class Meta:
        fields=['email','otp']
    def validate(self,data):
        email1=data.get("email","")
        otp1=data.get("otp","")
        new_password1=data.get("new_password","")
        email2=Detail.objects.filter(email=email1)
        if email2:
            email3=Detail.objects.get(email=email1)
            now = datetime.now()
            timestamp1 = datetime.timestamp(now)
            diff=abs(float(email3.timestamp)-timestamp1)
            print(diff)
            if diff<=60:
                if email3.otp==otp1:
                    Detail.objects.filter(email=email1).update(password=new_password1)
                    return data
                else:
                    raise serializers.ValidationError({
                                                    "status_type": "false",
                                                    "entity": [
                                                        {
                                                            "mail_id": email1
                                                        }
                                                    ],
                                                    "entity_type": "JsonArrays",
                                                    "entity_status": "1",
                                                    "entity_msg": "User OTP is invaild",
                                                    "status": "202"
                                                })
            else:
                raise serializers.ValidationError({
                                                "status_type": "false",
                                                "entity": [
                                                    {
                                                        "mail_id": email1
                                                    }
                                                ],
                                                "entity_type": "JsonArrays",
                                                "entity_status": "1",
                                                "entity_msg": "time out error",
                                                "status": "202"
                                            })

        else:
            raise serializers.ValidationError({
                                                "status_type": "false",
                                                "entity": [
                                                    {
                                                        "mail_id": email1
                                                    }
                                                ],
                                                "entity_type": "JsonArrays",
                                                "entity_status": "1",
                                                "entity_msg": "give a valid email id",
                                                "status": "202"
                                            })
