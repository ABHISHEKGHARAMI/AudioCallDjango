from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'
urlpatterns = [
     path('login/',views.user_login,name='login'),
     path('logout/',auth_views.LogoutView.as_view(),name='logout'),
     path('signup/',views.SignUpView.as_view(),name='signup'),
]
