from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('graphics/', views.graphics, name='graphics'),
    path('dash/', views.dash, name='dash'),
    path('login/', auth_views.LoginView.as_view(template_name='index.html'), name='login'),
    path('', views.index, name='index'),

]
