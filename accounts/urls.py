from django.urls import path

from .views import (user_registration, user_login, user_logout,
                    change_password,
                    user_profile, show_user_profile )

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register/', user_registration, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('password/', change_password, name='change_password'),
    path('profile/<int:profile_id>/', show_user_profile, name='show_user_profile'),

]
