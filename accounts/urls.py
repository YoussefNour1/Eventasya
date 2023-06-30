from django.urls import path

from accounts.views import SignUpAPIView, LoginView, UserDetailsAPIView, signup_verify, ForgotPasswordView,\
    ForgotPasswordVerifyView, ChangePasswordView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path('verify/', signup_verify, name="signup_verify"),
    path("login/", LoginView.as_view(), name="login"),
    path('users/me', UserDetailsAPIView.as_view(), name='user_update'),
    path('password/forget/', ForgotPasswordView.as_view(), name='forget-password'),
    path('password/confirmation/', ForgotPasswordVerifyView.as_view(), name='confirm-password'),
    path('password/change/', ChangePasswordView.as_view(), name='change-password'),
]

'''
/accounts/signup/ (POST) => user signup   {
    "email": "",
    "password": "",
    "first_name": "",
    "last_name": "",
    "role": null,
    "gender": null,
    "birthdate": null,
    "contact_number": "",
    "img": null
    }
/accounts/login/ (POST) => user login {"email": "", "password": ""}
/accounts/verify/ (POST) => email verification {"otp": ""}
/accounts/users/me (PUT/PATCH) => update user
'''
