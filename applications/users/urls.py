from django.urls import path

from . import views

app_name='users_app'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('api/login', views.GoogleLogin.as_view(), name='loginGoogle'),
]