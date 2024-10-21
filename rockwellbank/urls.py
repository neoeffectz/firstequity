from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about, name='about'),
    path('signin/', views.signin, name='signin'),
    path('portfolio/', views.portfolio, name = 'portfolio'),
    path('transfer/', views.transfer, name = 'transfer'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('logout', views.logout, name = 'logout'),
    
      
]
