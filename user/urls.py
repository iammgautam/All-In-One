from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('activate/<uidb64>/<token>/', views.activateEmail.as_view(), name='activate'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('resetPass/',views.RequestResetPass.as_view(), name='resetPass'),
    path('passReset/<uidb64>/<token>/', views.new_password.as_view(), name='password'),

    path('profile/', views.profile, name='profile'),
    path('profileForm/', views.profileEdit, name='profileEdit'),
    path('', views.home, name='home'),
]
