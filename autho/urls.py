from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("change-password/", views.change_password, name="change_password"),
    
    path("profile/", views.profile, name="profile"),
    # path("edit-profile/", views.edit_profile, name="edit_profile"),
    path('accounts/', include('allauth.urls')),
]