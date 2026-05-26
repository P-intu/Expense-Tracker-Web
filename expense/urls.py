from django.urls import path
from . import views
urlpatterns=[
    path('', views.home,name='home'),
    path('add/', views.add_expense,name='add_expense'),
    path('login/', views.login_user,name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('register/', views.register_user,name='register'),
    path('set/', views.set_income,name='set_income'),
    path('delete/<int:id>/', views.delete_expense,name='delete_expense'),
]