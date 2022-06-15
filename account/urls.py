from django.contrib import admin
from django.urls import path
from account import views

urlpatterns = [
    path("register/",views.UserRegistration.as_view(),name='register'),
    path("login/",views.UserLogin.as_view(),name="login"),
    path("profile/",views.UserProfile.as_view(),name="profile"),
    path("changepassword/",views.UserPasswordChange.as_view(),name="changepassword"),
    path("logout/",views.UserLogout.as_view(),name="logout"),
    # path("send-rest-password-email/",views.SendPasswordResetEmailView.as_view(),name="send-reset-password-email"),
    # path("reset-password/<uid>/<token>/",views.SavePasswordResetEmailView.as_view(),name="reset-password"),

]

