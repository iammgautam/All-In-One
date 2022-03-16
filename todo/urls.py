from django.urls import path
from todo import views

urlpatterns = [
    path('', views.homePage, name='todo-home'),
    path('add/',views.addTask, name='add-task'),
    path('search/', views.search, name='search'),
    path('update/<str:pk>/', views.updateTask, name='update-task'),
    path('<str:pk>/', views.detailTask, name='detail-task'),
    path('delete/<str:pk>/', views.deleteTask, name='delete-task'),
    
]
