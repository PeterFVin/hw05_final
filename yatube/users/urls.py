from django.contrib.auth import views
from django.urls import path

from users.views import SignUp

app_name = '%(app_label)s'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout',
    ),
    path(
        'login/',
        views.LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
        ),
        name='password_change',
    ),
    path(
        'password_change_done/',
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
]
