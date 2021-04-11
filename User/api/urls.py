from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token
from User.api.views import(
    register_view,login_view,update_view,otp_view,otpvalid_view
)
app_name="User"

urlpatterns = [
           path('register',register_view,name="register"),
           path('login',login_view,name="login"),
           path('update',update_view,name="update"),
           path('otp',otp_view,name="otp"),
           path('otpvalid',otpvalid_view,name="otpvalid")
]
