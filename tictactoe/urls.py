from django.contrib import admin
from django.urls import path, include
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #auth
    path('signup/', views.signup_user, name='signup_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    #game
    path('', views.home, name='home'),
    path('game/', include('game.urls')),
]
