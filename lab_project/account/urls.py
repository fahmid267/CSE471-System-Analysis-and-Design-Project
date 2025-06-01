from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name = "signup"),
    path('login', views.user_login, name = "login"),
    path('logout', views.user_logout, name = "logout"),
    path('verify_account', views.link_send, name = 'verify_account'),
    path('verify/<verf_link>', views.verify, name = "verify"),
    path('my_profile', views.my_profile, name = 'my_profile'), 
    path('update_profile', views.updateProfile, name = "update_profile"),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('verifipassword/<verf_link>/', views.verifipassword, name='verifipassword'),
    path('changepass/', views.changepass, name='changepass')
]