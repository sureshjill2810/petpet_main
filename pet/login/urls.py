from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Email confirmation URLs
    path('send_confirmation_email/', views.send_confirmation_email, name='send_confirmation_email'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),

    # Other views
    path('email_sent/', views.email_sent, name='email_sent'),
    path('account_activated/', views.account_activated, name='account_activated'),
    path('activation_failed/', views.activation_failed, name='activation_failed'),

    # Home URL
    path('', views.home, name='home'),
]
